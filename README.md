# 🏢 FB Real Estate Data Miner & CRM Mapper

A professional automation tool designed to extract, clean, and transform unstructured real estate data from Facebook Excel exports into a structured CRM-ready format. Specifically optimized for the **Jaipur Real Estate Market**.

## 🚀 Features

- **Automated Extraction**: Scans raw text to find:
  - **BHK Details**: Categorizes into 1 BHK, 2 BHK, or 3 BHK and above.
  - **Price Analysis**: Cleans and extracts pricing/rent information.
  - **Contact Info**: Intelligent Indian mobile number extraction.
  - **Location Mapping**: Recognizes specific Jaipur areas (Vaishali Nagar, Mansarovar, Jagatpura, etc.).
- **CRM Integration**: Maps data directly to standard CRM fields like Campaign, CustomerType, Area, and Address.
- **Smart Classification**: 
  - Automatically identifies **Campaigns** (Rentout, Seller, Buyer).
  - Categorizes **Customer Types** (Flat, House, Villa, Plot, Commercial, etc.).
- **User-Friendly Interface**: Built with Streamlit for a seamless drag-and-drop experience.

## 🛠️ Local Installation

If you want to run this project on your local machine:

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/your-username/fb-data-miner.git](https://github.com/your-username/fb-data-miner.git)
   cd fb-data-miner
