#!/usr/bin/env python3
# Script untuk menerjemahkan jurnal ke bahasa Inggris

import re

# Mapping terjemahan akun dari Indonesia ke Inggris
account_translations = {
    # Aset
    'Kas/Bank': 'Cash/Bank',
    'Piutang Usaha': 'Accounts Receivable',
    'Persediaan': 'Inventory',
    'Peralatan': 'Equipment',
    'Mesin': 'Machinery',
    'PPN Masukan': 'Input VAT',
    'PPh 22 Dibayar di Muka': 'Prepaid Income Tax Article 22',
    'PPh 25 Dibayar di Muka': 'Prepaid Income Tax Article 25',
    'Aset Pajak Tangguhan': 'Deferred Tax Asset',
    
    # Kewajiban
    'Utang Pajak Penghasilan': 'Income Tax Payable',
    'Utang PPh 21': 'Income Tax Article 21 Payable',
    'Utang PPh 23': 'Income Tax Article 23 Payable',
    'Utang PPh 26': 'Income Tax Article 26 Payable',
    'Utang PPh 29': 'Income Tax Article 29 Payable',
    'Utang PPh Final Pasal 4(2)': 'Final Income Tax Article 4(2) Payable',
    'Utang PPN Keluaran': 'Output VAT Payable',
    'Utang Bea Masuk': 'Import Duty Payable',
    'Kewajiban Pajak Tangguhan': 'Deferred Tax Liability',
    'Utang Pajak/Aset Pajak': 'Tax Payable/Tax Asset',
    
    # Ekuitas
    
    # Pendapatan
    'Penjualan': 'Sales',
    
    # Beban
    'Beban Pajak Penghasilan': 'Income Tax Expense',
    'Beban Gaji dan Upah': 'Salary and Wage Expense',
    'Beban Gaji': 'Salary Expense',
    'Beban Sewa Gedung': 'Building Rent Expense',
    'Beban Sewa Kendaraan': 'Vehicle Rent Expense',
    'Beban Royalti': 'Royalty Expense',
    'Beban PPh Pasal 15': 'Income Tax Article 15 Expense',
    'Beban PPN': 'VAT Expense',
    'Beban PBB': 'Land and Building Tax Expense',
    'Beban Bea Meterai': 'Stamp Duty Expense',
    'Beban Pajak Tangguhan': 'Deferred Tax Expense',
    'Beban Pajak Kini/Tangguhan': 'Current/Deferred Tax Expense',
}

# Mapping terjemahan keterangan
description_translations = {
    'Pengakuan beban pajak penghasilan tahun berjalan': 'Recognition of current year income tax expense',
    'Pembayaran gaji dengan pemotongan PPh 21': 'Salary payment with Article 21 income tax withholding',
    'Pembayaran sewa gedung dengan pemotongan PPh final': 'Building rent payment with final income tax withholding',
    'Pencatatan impor mesin dengan berbagai komponen pajak': 'Recording machinery import with various tax components',
    'Pembayaran sewa kendaraan dengan pemotongan PPh 23': 'Vehicle rent payment with Article 23 income tax withholding',
    'Pembayaran angsuran PPh Pasal 25 bulanan': 'Monthly installment payment of Article 25 income tax',
    'Pembayaran royalti kepada perusahaan asing dengan pemotongan PPh 26': 'Royalty payment to foreign company with Article 26 income tax withholding',
    'Pembayaran PPh Pasal 15 atas penghasilan pelayaran internasional': 'Payment of Article 15 income tax on international shipping income',
    'Pengakuan PPh kurang bayar tahun berjalan': 'Recognition of current year income tax underpayment',
    'Pencatatan penjualan dengan PPN': 'Recording sales with VAT',
    'Pembayaran Pajak Bumi dan Bangunan': 'Payment of Land and Building Tax',
    'Pembayaran Bea Meterai': 'Payment of Stamp Duty',
    'Pengakuan manfaat perencanaan pajak': 'Recognition of tax planning benefits',
    'Pencatatan sesuai prinsip akuntansi pajak': 'Recording according to tax accounting principles',
}

def translate_journal_entry(journal_text):
    """Menerjemahkan teks jurnal dari Indonesia ke Inggris"""
    lines = journal_text.strip().split('\n')
    translated_lines = []
    
    for line in lines:
        # Terjemahkan akun
        for indo, eng in account_translations.items():
            if indo in line:
                line = line.replace(indo, eng)
        
        # Format tetap sama, hanya terjemahkan teks
        translated_lines.append(line)
    
    return '\n'.join(translated_lines)

def translate_description(description):
    """Menerjemahkan keterangan jurnal"""
    # Hapus tanda kurung jika ada
    desc = description.strip()
    if desc.startswith('(') and desc.endswith(')'):
        desc = desc[1:-1]
    
    # Terjemahkan
    for indo, eng in description_translations.items():
        if indo in desc:
            return f'({eng})'
    
    # Jika tidak ditemukan terjemahan spesifik
    return f'({desc})'  # Biarkan asli jika tidak ada terjemahan

def process_file(input_file, output_file):
    """Memproses file dan menerjemahkan jurnal"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pola untuk menemukan blok jurnal
    # Mencari pola: **Jurnal:** diikuti oleh ``` ... ``` dan keterangan dalam ()
    pattern = r'(\*\*Jurnal:\*\*\s*\n```\n)(.*?)(\n```\s*\n)(\(.*?\))'
    
    def replace_journal(match):
        jurnal_label = match.group(1)  # **Jurnal:**\n```
        journal_content = match.group(2)  # isi jurnal
        closing_ticks = match.group(3)  # ```\n
        description = match.group(4)  # (keterangan)
        
        # Terjemahkan isi jurnal
        translated_journal = translate_journal_entry(journal_content)
        
        # Terjemahkan keterangan
        translated_desc = translate_description(description)
        
        return f"{jurnal_label}{translated_journal}{closing_ticks}{translated_desc}"
    
    # Lakukan penggantian
    new_content = re.sub(pattern, replace_journal, content, flags=re.DOTALL)
    
    # Tulis ke file output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"File telah diproses: {input_file} -> {output_file}")
    print(f"Jumlah terjemahan akun: {len(account_translations)}")
    print(f"Jumlah terjemahan keterangan: {len(description_translations)}")

if __name__ == "__main__":
    input_file = "soal_akuntansi_perpajakan_complete.md"
    output_file = "soal_akuntansi_perpajakan_english_journals.md"
    
    process_file(input_file, output_file)
    
    # Tampilkan contoh terjemahan
    print("\nContoh terjemahan:")
    print("=" * 50)
    print("Asli: [Debit] Beban Pajak Penghasilan     319.000.000")
    print("Terjemahan: [Debit] Income Tax Expense     319.000.000")
    print("\nAsli: [Kredit] Utang PPh 21                180.250.000")
    print("Terjemahan: [Kredit] Income Tax Article 21 Payable    180.250.000")
    print("\nAsli: (Pengakuan beban pajak penghasilan tahun berjalan)")
    print("Terjemahan: (Recognition of current year income tax expense)")