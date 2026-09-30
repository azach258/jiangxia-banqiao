/**
 * =========================================================================
 * 江夏傳統整復推拿（板橋館）- Google 日曆與試算表雙向預約雲端橋樑 (GAS)
 * =========================================================================
 * 
 * 【主要功能】：
 * 1. 雙向同步：顧客線上預約即時寫入 Google 日曆，日曆行程即時反映至後台。
 * 2. Telegram 即時推播：顧客送出預約，賴師傅手機 Telegram 立刻收到推播提醒。
 * 3. 永久記帳：可自動同步將預約寫入 Google Sheets 試算表留存。
 * 4. 遠端銷毀：後台點擊刪除，同步自 Google 日曆移除事件。
 */

var API_SECRET = 'jiangxia_banqiao_2026';
var TARGET_CALENDAR_NAME = '江夏傳統整復推拿_板橋館';

// Telegram Bot 即時推播設定 (新預約立即叮咚通知師傅手機)
var TG_BOT_TOKEN = '7789811491:AAG2c7qWuhB2yIacI6_KSsZrXjRCcvClWcI';
var TG_CHAT_ID = '1890470289';

// (選配) Google 試算表 ID：若有建立專屬試算表，填入試算表網址中的 ID，留空則自動使用當前試算表
var SPREADSHEET_ID = '';

// 取得目標日曆（自動尋找「江夏傳統整復推拿_板橋館」，找不到則模糊搜尋，最後退回主日曆）
function getTargetCalendar() {
  if (TARGET_CALENDAR_NAME) {
    var cals = CalendarApp.getCalendarsByName(TARGET_CALENDAR_NAME);
    if (cals && cals.length > 0) {
      return cals[0];
    }
    var all = CalendarApp.getAllCalendars();
    for (var i = 0; i < all.length; i++) {
      if (all[i].getName().indexOf('江夏') !== -1) {
        return all[i];
      }
    }
  }
  return CalendarApp.getDefaultCalendar();
}

// 發送 Telegram 即時推播通知
function sendTelegramNotification(text) {
  if (!TG_BOT_TOKEN || !TG_CHAT_ID) return;
  try {
    var url = 'https://api.telegram.org/bot' + TG_BOT_TOKEN + '/sendMessage';
    var payload = {
      chat_id: TG_CHAT_ID,
      text: text,
      parse_mode: 'HTML',
      disable_web_page_preview: true
    };
    UrlFetchApp.fetch(url, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });
  } catch (e) {
    Logger.log('Telegram 通知發送失敗: ' + e.toString());
  }
}

// ==========================================
// 1. GET 請求處理 (Ping 診斷、拉取預約、刪除預約)
// ==========================================
function doGet(e) {
  try {
    var params = (e && e.parameter) ? e.parameter : {};
    var secret = params.secret || '';
    var action = params.action || 'ping';

    if (secret !== API_SECRET && action !== 'ping') {
      return createJsonResponse({ success: false, message: '未授權的安全金鑰' });
    }

    var cal = getTargetCalendar();

    // 1-1. 連線檢測
    if (action === 'ping') {
      var now = new Date();
      var startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0);
      var endOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59);
      var todayEvents = cal.getEvents(startOfDay, endOfDay);

      var hasSpreadsheet = false;
      try {
        var ss = SPREADSHEET_ID ? SpreadsheetApp.openById(SPREADSHEET_ID) : SpreadsheetApp.getActiveSpreadsheet();
        if (ss) hasSpreadsheet = true;
      } catch (err) {
        hasSpreadsheet = false;
      }

      return createJsonResponse({
        success: true,
        message: 'Google 雲端橋樑運作正常！',
        diagnostics: {
          calendarName: cal ? cal.getName() : '主要日曆',
          serverTime: Utilities.formatDate(now, 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss'),
          todayEventsCount: todayEvents.length,
          hasSpreadsheet: hasSpreadsheet,
          hasTelegram: !!(TG_BOT_TOKEN && TG_CHAT_ID)
        }
      });
    }

    // 1-2. 抓取預約列表
    if (action === 'getEvents') {
      var now = new Date();
      var startTime = new Date(now.getTime() - 3 * 24 * 60 * 60 * 1000);
      var endTime = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000);
      var events = cal.getEvents(startTime, endTime);

      var data = [];
      for (var i = 0; i < events.length; i++) {
        var evt = events[i];
        var title = (evt.getTitle() || '').trim();
        var desc = evt.getDescription() || '';

        var customerName = title;
        var phone = '';

        var titleParts = title.split(/\s+/);
        if (titleParts.length >= 2 && /^[0-9-]+$/.test(titleParts[titleParts.length - 1])) {
          phone = titleParts[titleParts.length - 1];
          customerName = titleParts.slice(0, titleParts.length - 1).join(' ');
        } else if (title.indexOf('【預約】') !== -1) {
          customerName = title.replace('【預約】', '').split('-')[0].trim();
        }

        var serviceItem = '徒手調理放鬆';
        var status = '已確認';

        var phoneMatch = desc.match(/電話[:：]\s*([0-9-]+)/);
        if (phoneMatch && !phone) phone = phoneMatch[1].trim();

        var serviceMatch = desc.match(/項目[:：]\s*([^\n\r]+)/);
        if (serviceMatch) serviceItem = serviceMatch[1].trim();

        var statusMatch = desc.match(/狀態[:：]\s*([^\n\r]+)/);
        if (statusMatch) status = statusMatch[1].trim();

        var startIso = Utilities.formatDate(evt.getStartTime(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss').replace(' ', 'T');
        var endIso = Utilities.formatDate(evt.getEndTime(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss').replace(' ', 'T');

        data.push({
          id: evt.getId(),
          customerName: customerName,
          phone: phone,
          serviceItem: serviceItem,
          status: status,
          notes: desc,
          start: startIso,
          end: endIso
        });
      }

      return createJsonResponse({
        success: true,
        count: data.length,
        data: data
      });
    }

    // 1-3. 刪除預約行程 (支援 deleteEvent / delete / cancel)
    if (action === 'deleteEvent' || action === 'delete' || action === 'cancel') {
      var eventId = params.eventId || params.id;
      if (!eventId) {
        return createJsonResponse({ success: false, message: '缺少 eventId 或 id' });
      }
      try {
        var evt = cal.getEventById(eventId);
        if (!evt && eventId.indexOf('@google.com') === -1) {
          evt = cal.getEventById(eventId + '@google.com');
        }
        if (!evt && eventId.indexOf('@google.com') !== -1) {
          evt = cal.getEventById(eventId.replace('@google.com', ''));
        }
        if (evt) {
          var delTitle = evt.getTitle();
          var delStart = Utilities.formatDate(evt.getStartTime(), 'Asia/Taipei', 'yyyy/MM/dd (E) HH:mm');
          evt.deleteEvent();

          // 刪除時亦推播提醒師傅
          try {
            var tgDelMsg = '🗑️ <b>【江夏板橋館・預約取消/刪除提醒】</b>\n' +
              '━━━━━━━━━━━━━━━\n' +
              '👤 <b>排程資訊</b>：' + delTitle + '\n' +
              '📅 <b>原約時段</b>：' + delStart + '\n' +
              '━━━━━━━━━━━━━━━\n' +
              '<i>該時段已重新釋出為可預約空檔。</i>';
            sendTelegramNotification(tgDelMsg);
          } catch(e) {}

          return createJsonResponse({
            success: true,
            message: '已成功從 Google 日曆刪除行程！',
            eventId: eventId
          });
        } else {
          return createJsonResponse({
            success: true,
            message: '日曆上已無該行程 (可能已手動刪除)',
            eventId: eventId
          });
        }
      } catch (delErr) {
        return createJsonResponse({
          success: false,
          error: '刪除日曆事件失敗: ' + delErr.toString()
        });
      }
    }

    return createJsonResponse({ success: false, message: '未知的 GET 操作指令: ' + action });

  } catch (error) {
    return createJsonResponse({ success: false, error: error.toString() });
  }
}

// ==========================================
// 2. POST 請求處理 (建立預約 ＆ 備援刪除)
// ==========================================
function doPost(e) {
  try {
    var payload = {};
    if (e && e.postData && e.postData.contents) {
      try {
        payload = JSON.parse(e.postData.contents);
      } catch (err) {
        payload = (e && e.parameter) ? e.parameter : {};
      }
    } else if (e && e.parameter) {
      payload = e.parameter;
    }

    var secret = payload.secret || '';
    if (secret !== API_SECRET) {
      return createJsonResponse({ success: false, message: '未授權的安全金鑰' });
    }

    var action = payload.action || 'create';

    // 2-1. 建立預約
    if (action === 'create') {
      var customerName = (payload.customerName || '顧客').trim();
      var phone = (payload.phone || '').trim();
      var serviceItem = payload.serviceItem || '傳統全身整復放鬆調理';
      var durationMin = parseInt(payload.durationMin || 60, 10);
      var startTimeStr = payload.startTime;
      var notes = payload.notes || '';
      var staff = payload.staff || '賴師傅';
      var status = payload.status || '已確認';

      if (!startTimeStr) {
        return createJsonResponse({ success: false, message: '缺少開始時間 startTime' });
      }

      var start = new Date(startTimeStr);
      var end = new Date(start.getTime() + durationMin * 60 * 1000);

      var cal = getTargetCalendar();
      var eventTitle = customerName + (phone ? ' ' + phone : '');
      
      var eventDescription = '顧客姓名：' + customerName + '\n' +
        '聯絡電話：' + phone + '\n' +
        '預約項目：' + serviceItem + '\n' +
        '預約時長：' + durationMin + ' 分鐘\n' +
        '服務師傅：' + staff + '\n' +
        '預約狀態：' + status + '\n' +
        '備註說明：' + notes + '\n' +
        '建立時間：' + Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss');

      var event = cal.createEvent(eventTitle, start, end, {
        description: eventDescription,
        location: '新北市板橋區館前西路152號之1'
      });

      // 自動備份寫入 Google 試算表 (若有設定 SPREADSHEET_ID 或為試算表綁定專案)
      try {
        var ss = SPREADSHEET_ID ? SpreadsheetApp.openById(SPREADSHEET_ID) : SpreadsheetApp.getActiveSpreadsheet();
        if (ss) {
          var sheet = ss.getSheetByName('預約紀錄名冊');
          if (!sheet) {
            sheet = ss.insertSheet('預約紀錄名冊');
            sheet.appendRow(['預約時間', '結束時間', '顧客姓名', '手機號碼', '調理項目', '時長(分)', '服務師傅', '狀態', '備註說明', '日曆事件ID']);
            sheet.getRange(1, 1, 1, 10).setFontWeight('bold').setBackground('#FAF7F2');
          }
          sheet.appendRow([
            Utilities.formatDate(start, 'Asia/Taipei', 'yyyy-MM-dd HH:mm'),
            Utilities.formatDate(end, 'Asia/Taipei', 'yyyy-MM-dd HH:mm'),
            customerName,
            phone,
            serviceItem,
            durationMin,
            staff,
            status,
            notes,
            event.getId()
          ]);
        }
      } catch (sheetErr) {
        Logger.log('試算表非致命錯誤: ' + sheetErr.toString());
      }

      // 即時推播通知賴師傅的手機 Telegram
      try {
        var startFormatted = Utilities.formatDate(start, 'Asia/Taipei', 'yyyy/MM/dd (E) HH:mm');
        var tgMsg = '🔔 <b>【江夏板橋館・新線上預約通報】</b>\n' +
          '━━━━━━━━━━━━━━━\n' +
          '👤 <b>顧客姓名</b>：' + customerName + '\n' +
          '📱 <b>聯絡電話</b>：' + (phone || '未填寫') + '\n' +
          '💆 <b>預約方案</b>：' + serviceItem + '\n' +
          '⏱️ <b>預約時長</b>：' + durationMin + ' 分鐘\n' +
          '📅 <b>預約時段</b>：' + startFormatted + '\n' +
          '📝 <b>顧客備註</b>：' + (notes || '無') + '\n' +
          '━━━━━━━━━━━━━━━\n' +
          '👉 <a href="https://azach258.github.io/jiangxia-banqiao/dashboard/">點此開啟師傅排程看板</a>';
        sendTelegramNotification(tgMsg);
      } catch (tgErr) {
        Logger.log('Telegram 通知非致命錯誤: ' + tgErr.toString());
      }

      var formattedStart = Utilities.formatDate(start, 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss');
      return createJsonResponse({
        success: true,
        message: '預約已成功寫入 Google 日曆與試算表！',
        calendarName: cal.getName(),
        eventTitle: eventTitle,
        eventId: event.getId(),
        start: formattedStart
      });
    }

    // 2-2. 刪除預約
    if (action === 'deleteEvent' || action === 'delete' || action === 'cancel') {
      var eventId = payload.eventId || payload.id;
      var cal = getTargetCalendar();
      if (!eventId) {
        return createJsonResponse({ success: false, message: '缺少 eventId 或 id' });
      }
      try {
        var evt = cal.getEventById(eventId);
        if (!evt && eventId.indexOf('@google.com') === -1) {
          evt = cal.getEventById(eventId + '@google.com');
        }
        if (!evt && eventId.indexOf('@google.com') !== -1) {
          evt = cal.getEventById(eventId.replace('@google.com', ''));
        }
        if (evt) {
          var pDelTitle = evt.getTitle();
          var pDelStart = Utilities.formatDate(evt.getStartTime(), 'Asia/Taipei', 'yyyy/MM/dd (E) HH:mm');
          evt.deleteEvent();

          try {
            var tgPDelMsg = '🗑️ <b>【江夏板橋館・預約取消/刪除提醒】</b>\n' +
              '━━━━━━━━━━━━━━━\n' +
              '👤 <b>排程資訊</b>：' + pDelTitle + '\n' +
              '📅 <b>原約時段</b>：' + pDelStart + '\n' +
              '━━━━━━━━━━━━━━━\n' +
              '<i>該時段已重新釋出為可預約空檔。</i>';
            sendTelegramNotification(tgPDelMsg);
          } catch(e) {}

          return createJsonResponse({
            success: true,
            message: '已成功從 Google 日曆刪除行程！',
            eventId: eventId
          });
        } else {
          return createJsonResponse({
            success: true,
            message: '日曆上已無該行程 (可能已手動刪除)',
            eventId: eventId
          });
        }
      } catch (err) {
        return createJsonResponse({
          success: false,
          error: '刪除日曆事件失敗: ' + err.toString()
        });
      }
    }

    return createJsonResponse({ success: false, message: '未知的 POST 操作指令: ' + action });

  } catch (error) {
    return createJsonResponse({ success: false, error: error.toString() });
  }
}

// ==========================================
// 3. 通用 JSON 回應處理
// ==========================================
function createJsonResponse(data) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

// ==========================================
// 4. 測試診斷專用 (若在 GAS 介面按「執行」，請選此函式)
// ==========================================
function test_run_diagnostics() {
  var res = doGet({ parameter: { action: 'ping', secret: API_SECRET } });
  Logger.log(res.getContent());
}
