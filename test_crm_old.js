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

  // Old implementation
  deleteCustomerConfirm(origPhone) {
    const cleanOrig = origPhone.replace(/[^0-9]/g, '');
    if (cleanOrig && !this.deletedCustomerPhones.includes(cleanOrig)) {
      this.deletedCustomerPhones.push(cleanOrig);
    }
    this.customers = this.customers.filter(c => {
      if (cleanOrig && c.phone && (c.phone || "").replace(/[^0-9]/g, '') === cleanOrig) return false;
      return true;
    });
  }

  fetchFromCloud(sheetPhone) {
    // old clean phone logic
    const cleanPhone = sheetPhone.replace(/[^0-9]/g, '');
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

      if (!phoneMap.has(phoneKey)) {
        phoneMap.set(phoneKey, { name: c.name, phone: rawPhone });
      }
    });

    this.customers = Array.from(phoneMap.values());
  }
}

const app = new CRM();
app.deleteCustomerConfirm('900111222');
console.log('Blocklist contains:', app.deletedCustomerPhones);

app.fetchFromCloud('900111222');
console.log('After background sync, customers:', app.customers);
