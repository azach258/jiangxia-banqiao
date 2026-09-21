/**
 * ==============================================================================
 * 江夏傳統整復推拿（板橋館）｜Google Calendar 雲端預約中繼 API (Google Apps Script)
 * ==============================================================================
 * 
 * 部署說明：
 * 1. 前往 https://script.google.com/ 建立新專案。
 * 2. 清空原本的 Code.gs，將本檔案內容完整貼上。
 * 3. 修改下方 CONFIG 中的 CALENDAR_ID (通常為您的 Google 帳號 Email，或獨立的「江夏預約日曆」ID)。
 * 4. 點選右上角「部署」 > 「新增部署作業」。
 * 5. 齒輪選擇「網頁應用程式 (Web app)」。
 *    - 說明：江夏預約系統 API v1
 *    - 執行身分：我 (您的 Google 帳號)
 *    - 誰可以存取：任何人 (Anyone)  <-- 必須選此項前端才能免登入呼叫
 * 6. 點選「部署」並授予日曆存取權限。
 * 7. 複製取得的「網頁應用程式網址 (Web app URL)」，貼回 HTML 儀表板的 API 設定中。
 */

const CONFIG = {
  // 日曆 ID：填寫 primary (主要日曆) 或特定日曆 ID (如 xxxxx@group.calendar.google.com)
  CALENDAR_ID: 'primary',
  
  // 安全金鑰 (可自訂，前端需在 Header 或 Query Param 帶入，設為空字串則不校驗)
  API_SECRET: 'jiangxia_banqiao_2026',
  
  // (選配) 若有 Google 試算表 ID，可同步寫入做永久預約存檔與顧客名冊；若不需要留空 ''
  SPREADSHEET_ID: '',
  SHEET_NAME: '預約總表'
};

/**
 * 處理 GET 請求 (查詢預約、檢查時段衝突)
 */
function doGet(e) {
  try {
    const params = e.parameter || {};
    
    // 簡單安全密鑰校驗
    if (CONFIG.API_SECRET && params.secret !== CONFIG.API_SECRET) {
      return createJsonResponse({ success: false, message: '未經授權的存取 (無效的 API Secret)' }, 403);
    }
    
    const action = params.action || 'getEvents';
    
    if (action === 'ping') {
      const cal = CalendarApp.getCalendarById(CONFIG.CALENDAR_ID);
      if (!cal) {
        return createJsonResponse({ success: false, message: 'API 授權金鑰正確，但找不到指定的 Google 日曆：' + CONFIG.CALENDAR_ID }, 404);
      }
      const today = new Date();
      const todayStart = new Date(today.getFullYear(), today.getMonth(), today.getDate());
      const todayEnd = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1);
      const todayEvents = cal.getEvents(todayStart, todayEnd);

      return createJsonResponse({
        success: true,
        message: 'Google Calendar API 雙向連線正常！',
        diagnostics: {
          calendarName: cal.getName(),
          timeZone: cal.getTimeZone(),
          calendarId: CONFIG.CALENDAR_ID,
          todayEventsCount: todayEvents.length,
          serverTime: Utilities.formatDate(new Date(), 'GMT+8', 'yyyy-MM-dd HH:mm:ss'),
          hasSpreadsheet: !!CONFIG.SPREADSHEET_ID
        }
      });
    }

    if (action === 'getEvents') {
      // 預設查詢前後 30 天
      const now = new Date();
      const startStr = params.start || new Date(now.getTime() - 15 * 24 * 60 * 60 * 1000).toISOString();
      const endStr = params.end || new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000).toISOString();
      
      const startTime = new Date(startStr);
      const endTime = new Date(endStr);
      
      const cal = CalendarApp.getCalendarById(CONFIG.CALENDAR_ID);
      if (!cal) {
        return createJsonResponse({ success: false, message: '找不到指定的 Google 日曆：' + CONFIG.CALENDAR_ID }, 404);
      }
      
      const events = cal.getEvents(startTime, endTime);
      const list = events.map(function(evt) {
        return parseEventData(evt);
      });
      
      return createJsonResponse({ success: true, data: list, count: list.length });
    }
    
    if (action === 'checkConflict') {
      const startTime = new Date(params.start);
      const endTime = new Date(params.end);
      const excludeEventId = params.excludeId || '';
      
      const cal = CalendarApp.getCalendarById(CONFIG.CALENDAR_ID);
      const events = cal.getEvents(startTime, endTime);
      
      // 排除全天事件或目前自己要修改的事件
      const conflicts = events.filter(function(evt) {
        if (evt.isAllDayEvent()) return false;
        if (excludeEventId && evt.getId() === excludeEventId) return false;
        return true;
      });
      
      return createJsonResponse({
        success: true,
        hasConflict: conflicts.length > 0,
        conflictCount: conflicts.length,
        conflicts: conflicts.map(function(evt) { return { id: evt.getId(), title: evt.getTitle(), start: evt.getStartTime().toISOString(), end: evt.getEndTime().toISOString() }; })
      });
    }
    
    return createJsonResponse({ success: false, message: '不支援的 GET 動作: ' + action }, 400);
  } catch (err) {
    return createJsonResponse({ success: false, error: err.toString() }, 500);
  }
}

/**
 * 處理 POST 請求 (新增預約、修改狀態、取消預約)
 */
function doPost(e) {
  try {
    let payload = {};
    if (e.postData && e.postData.contents) {
      payload = JSON.parse(e.postData.contents);
    } else {
      payload = e.parameter || {};
    }
    
    // 安全密鑰驗證
    if (CONFIG.API_SECRET && payload.secret !== CONFIG.API_SECRET) {
      return createJsonResponse({ success: false, message: '未經授權的存取 (無效的 API Secret)' }, 403);
    }
    
    const action = payload.action || 'create';
    const cal = CalendarApp.getCalendarById(CONFIG.CALENDAR_ID);
    if (!cal) {
      return createJsonResponse({ success: false, message: '找不到指定的 Google 日曆' }, 404);
    }
    
    // 1. 新增預約
    if (action === 'create') {
      const customerName = payload.customerName || '未知顧客';
      const phone = payload.phone || '';
      const serviceItem = payload.serviceItem || '傳統整復推拿放鬆';
      const durationMin = parseInt(payload.durationMin || 60, 10);
      const startTime = new Date(payload.startTime);
      const endTime = new Date(startTime.getTime() + durationMin * 60 * 1000);
      const notes = payload.notes || '';
      const staff = payload.staff || '賴師傅';
      const status = payload.status || '已確認';
      
      // 衝突檢查
      const existingEvents = cal.getEvents(startTime, endTime).filter(function(evt) {
        return !evt.isAllDayEvent();
      });
      if (existingEvents.length > 0 && !payload.force) {
        return createJsonResponse({
          success: false,
          conflict: true,
          message: '該時段已存在其他行程/預約，無法重複預約！'
        }, 409);
      }
      
      // 建立 Google Calendar 標題與描述
      const title = '【' + status + '】' + customerName + ' - ' + serviceItem;
      const description = [
        '【江夏傳統整復推拿板橋館 預約單】',
        '顧客姓名：' + customerName,
        '聯絡電話：' + phone,
        '服務項目：' + serviceItem + ' (' + durationMin + ' 分鐘)',
        '主治師傅：' + staff,
        '預約狀態：' + status,
        '備註說明：' + (notes || '無'),
        '建立時間：' + Utilities.formatDate(new Date(), 'GMT+8', 'yyyy-MM-dd HH:mm:ss')
      ].join('\n');
      
      const newEvent = cal.createEvent(title, startTime, endTime, {
        description: description,
        location: '新北市板橋區館前西路152-1號 (江夏傳統整復推拿)'
      });
      
      // 同步備份至 Google 試算表 (若有設定)
      logToSpreadsheet({
        id: newEvent.getId(),
        name: customerName,
        phone: phone,
        service: serviceItem,
        staff: staff,
        start: startTime,
        duration: durationMin,
        notes: notes,
        status: status
      });
      
      return createJsonResponse({
        success: true,
        message: '預約已成功寫入 Google 日曆',
        event: parseEventData(newEvent)
      });
    }
    
    // 2. 更新預約 (更新時間或狀態)
    if (action === 'update') {
      const eventId = payload.id;
      if (!eventId) return createJsonResponse({ success: false, message: '缺少預約 ID (id)' }, 400);
      
      const event = cal.getEventById(eventId);
      if (!event) return createJsonResponse({ success: false, message: '在日曆中找不到該預約事件' }, 404);
      
      if (payload.title) event.setTitle(payload.title);
      if (payload.notes || payload.description) event.setDescription(payload.notes || payload.description);
      if (payload.startTime && payload.endTime) {
        event.setTime(new Date(payload.startTime), new Date(payload.endTime));
      }
      
      return createJsonResponse({
        success: true,
        message: '預約已更新',
        event: parseEventData(event)
      });
    }
    
    // 3. 取消/刪除預約
    if (action === 'delete') {
      const eventId = payload.id;
      if (!eventId) return createJsonResponse({ success: false, message: '缺少預約 ID (id)' }, 400);
      
      const event = cal.getEventById(eventId);
      if (!event) return createJsonResponse({ success: false, message: '找不到該預約' }, 404);
      
      event.deleteEvent();
      return createJsonResponse({ success: true, message: '預約已從 Google 日曆刪除' });
    }
    
    // 4. 儲存顧客調理紀錄卡 (Care Record)
    if (action === 'saveRecord') {
      const eventId = payload.id;
      if (!eventId) return createJsonResponse({ success: false, message: '缺少預約 ID (id)' }, 400);
      
      const event = cal.getEventById(eventId);
      if (!event) return createJsonResponse({ success: false, message: '找不到該預約' }, 404);
      
      const record = payload.record || {};
      const currentDesc = event.getDescription() || '';
      
      // 將調理紀錄序列化為標籤區塊嵌入 Description
      const cleanDesc = currentDesc.replace(/\n\n---【江夏調理紀錄卡】[\s\S]*$/, '');
      const recordBlock = '\n\n---【江夏調理紀錄卡】---\n' + JSON.stringify(record, null, 2);
      event.setDescription(cleanDesc + recordBlock);
      
      // 若狀態需變更為已完成
      if (payload.status) {
        const title = event.getTitle().replace(/^【[^】]+】/, '【' + payload.status + '】');
        event.setTitle(title);
      }
      
      // 同步備份至試算表 (若有設定)
      logCareRecordToSpreadsheet(eventId, payload.customerName, payload.phone, record);
      
      return createJsonResponse({
        success: true,
        message: '顧客調理紀錄已成功保存',
        event: parseEventData(event)
      });
    }
    
    return createJsonResponse({ success: false, message: '不支援的 POST 動作: ' + action }, 400);
  } catch (err) {
    return createJsonResponse({ success: false, error: err.toString() }, 500);
  }
}

/**
 * 解析 Google 日曆事件為前端標準資料格式
 */
function parseEventData(evt) {
  const desc = evt.getDescription() || '';
  const title = evt.getTitle() || '';
  
  // 嘗試從 Description 提取姓名與電話
  let phone = '';
  let customerName = title;
  let serviceItem = '';
  let status = '已確認';
  let notes = '';
  let record = null;
  
  const phoneMatch = desc.match(/聯絡電話：([^\n]+)/);
  if (phoneMatch) phone = phoneMatch[1].trim();
  
  const nameMatch = desc.match(/顧客姓名：([^\n]+)/);
  if (nameMatch) customerName = nameMatch[1].trim();
  
  const serviceMatch = desc.match(/服務項目：([^\n]+)/);
  if (serviceMatch) serviceItem = serviceMatch[1].trim();
  
  const statusMatch = desc.match(/預約狀態：([^\n]+)/);
  if (statusMatch) status = statusMatch[1].trim();
  
  const notesMatch = desc.match(/備註說明：([^\n]+)/);
  if (notesMatch) notes = notesMatch[1].trim();
  
  // 提取調理紀錄卡 JSON
  const recordMatch = desc.match(/---【江夏調理紀錄卡】---\n([\s\S]+)$/);
  if (recordMatch) {
    try {
      record = JSON.parse(recordMatch[1].trim());
    } catch (e) {
      Logger.log('解析調理紀錄卡 JSON 失敗: ' + e);
    }
  }

  // 提取實收費用與付款方式
  let price = 0;
  let paymentMethod = '現金';
  if (record && record.price !== undefined) {
    price = parseInt(record.price, 10);
  } else {
    const priceMatch = desc.match(/實收費用：NT\$\s*(\d+)/) || desc.match(/費用金額：NT\$\s*(\d+)/);
    if (priceMatch) price = parseInt(priceMatch[1], 10);
  }

  if (record && record.paymentMethod) {
    paymentMethod = record.paymentMethod;
  } else {
    const payMatch = desc.match(/付款方式：([^\n]+)/);
    if (payMatch) paymentMethod = payMatch[1].trim();
  }
  
  return {
    id: evt.getId(),
    title: title,
    customerName: customerName,
    phone: phone,
    serviceItem: serviceItem,
    status: status,
    notes: notes,
    record: record,
    price: price,
    paymentMethod: paymentMethod,
    start: evt.getStartTime().toISOString(),
    end: evt.getEndTime().toISOString(),
    isAllDay: evt.isAllDayEvent(),
    description: desc,
    location: evt.getLocation()
  };
}

/**
 * 建立標準 JSON 回應與 CORS 支援
 */
function createJsonResponse(data, statusCode) {
  const output = ContentService.createTextOutput(JSON.stringify(data));
  output.setMimeType(ContentService.MimeType.JSON);
  return output;
}

/**
 * (選用) 將預約紀錄同步寫入 Google 試算表
 */
function logToSpreadsheet(info) {
  if (!CONFIG.SPREADSHEET_ID) return;
  try {
    const ss = SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID);
    let sheet = ss.getSheetByName(CONFIG.SHEET_NAME);
    if (!sheet) {
      sheet = ss.insertSheet(CONFIG.SHEET_NAME);
      sheet.appendRow(['事件ID', '登記時間', '顧客姓名', '電話', '服務項目', '主治師傅', '預約時段', '時長(分)', '狀態', '備註']);
    }
    sheet.appendRow([
      info.id,
      Utilities.formatDate(new Date(), 'GMT+8', 'yyyy-MM-dd HH:mm:ss'),
      info.name,
      info.phone,
      info.service,
      info.staff,
      Utilities.formatDate(info.start, 'GMT+8', 'yyyy-MM-dd HH:mm'),
      info.duration,
      info.status,
      info.notes
    ]);
  } catch (e) {
    Logger.log('寫入試算表失敗: ' + e.toString());
  }
}

/**
 * (選用) 將顧客到店調理紀錄卡同步寫入 Google 試算表
 */
function logCareRecordToSpreadsheet(eventId, customerName, phone, record) {
  if (!CONFIG.SPREADSHEET_ID) return;
  try {
    const ss = SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID);
    const sheetName = '顧客調理紀錄簿';
    let sheet = ss.getSheetByName(sheetName);
    if (!sheet) {
      sheet = ss.insertSheet(sheetName);
      sheet.appendRow(['事件ID', '記錄時間', '顧客姓名', '聯絡電話', '不適部位自述', '緊繃等級(1-10)', '調理重點手法', '實收費用(NT$)', '付款方式', '改善反饋', '居家保養建議', '補充筆記']);
    }
    sheet.appendRow([
      eventId,
      Utilities.formatDate(new Date(), 'GMT+8', 'yyyy-MM-dd HH:mm:ss'),
      customerName || '',
      phone || '',
      Array.isArray(record.complaints) ? record.complaints.join('、') : (record.complaints || ''),
      record.painLevel || '',
      Array.isArray(record.techniques) ? record.techniques.join('、') : (record.techniques || ''),
      record.price || 0,
      record.paymentMethod || '現金',
      record.feedback || '',
      record.homeAdvice || '',
      record.additionalNotes || ''
    ]);
  } catch (e) {
    Logger.log('寫入調理紀錄表失敗: ' + e.toString());
  }
}
