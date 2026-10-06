class CRM {
  constructor() {
    this.customers = [
      { id: '1', name: 'QA測試員', phone: '900111222' }
    ];
    this.bookings = [];
    this.deletedCustomerPhones = [];
  }
  
  getCleanPhoneKey(rawPhone) {
    if (!rawPhone || typeof rawPhone !== 'string') return '';
    let digits = rawPhone.replace(/[^0-9]/g, '');
    if (digits.startsWith('886') && digits.length >= 11) {
      digits = '0' + digits.slice(3);
    } else if (digits.length === 9 && digits.startsWith('9')) {
      digits = '0' + digits;
    }
    return digits;
  }

  formatStandardPhone(rawPhone) {
    if (!rawPhone) return '';
    const digits = String(rawPhone).replace(/[^0-9]/g, '');
    if (digits.length === 10 && digits.startsWith('09')) {
      return digits.slice(0, 4) + '-' + digits.slice(4, 7) + '-' + digits.slice(7);
    }
    return rawPhone;
  }

  deleteCustomerConfirm(origPhone) {
    const cleanOrig = this.getCleanPhoneKey(origPhone);
    if (cleanOrig && !this.deletedCustomerPhones.includes(cleanOrig)) {
      this.deletedCustomerPhones.push(cleanOrig);
    }
    this.customers = this.customers.filter(c => {
      if (cleanOrig && c.phone && this.getCleanPhoneKey(c.phone) === cleanOrig) return false;
      return true;
    });
  }

  fetchFromCloud(sheetPhone) {
    const cleanPhone = this.getCleanPhoneKey(sheetPhone);
    let cust = this.customers.find(c => this.getCleanPhoneKey(c.phone) === cleanPhone);
    if (!cust) {
      this.customers.push({
        name: 'QA測試員',
        phone: sheetPhone
      });
    }
    this.consolidateCustomersByPhone();
  }

  consolidateCustomersByPhone() {
    const phoneMap = new Map();
    this.customers.forEach(c => {
      const rawPhone = c.phone || '';
      const phoneKey = this.getCleanPhoneKey(rawPhone);

      if (!phoneKey) return;
      if (this.deletedCustomerPhones.includes(phoneKey)) return;

      const standardPhone = this.formatStandardPhone(rawPhone);
      if (!phoneMap.has(phoneKey)) {
        phoneMap.set(phoneKey, { name: c.name, phone: standardPhone });
      }
    });

    this.customers = Array.from(phoneMap.values());
  }
}

const app = new CRM();
console.log('Initial customers:', app.customers);
app.deleteCustomerConfirm('900111222');
console.log('After delete:', app.customers);
console.log('Blocklist:', app.deletedCustomerPhones);

app.fetchFromCloud('900111222');
console.log('After fetchFromCloud (900111222):', app.customers);

app.fetchFromCloud('0900111222');
console.log('After fetchFromCloud (0900111222):', app.customers);

app.fetchFromCloud(900111222); // AS A NUMBER TYPE
console.log('After fetchFromCloud (number 900111222):', app.customers);

