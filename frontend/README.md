# Frontend - React Application

This directory contains the React (Vite) frontend for the AI-Powered POS Account Hierarchy & Reporting Tool.

## Structure (Planned)

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── FileUpload.tsx
│   │   ├── AccountTable.tsx
│   │   └── ReportDashboard.tsx
│   ├── pages/               # Page components
│   │   ├── UploadPage.tsx
│   │   ├── AccountsPage.tsx
│   │   └── ReportsPage.tsx
│   ├── services/            # API clients
│   │   └── api.ts
│   ├── types/               # TypeScript type definitions
│   │   └── index.ts
│   ├── utils/               # Utility functions
│   │   └── index.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── public/
├── package.json
├── vite.config.ts
├── tsconfig.json
├── Dockerfile
└── README.md               # This file
```

## Key Features (Planned)

### File Upload Interface
- Excel file upload (.xlsx, .xls)
- Upload progress and status feedback
- Processing status tracking

### Reporting Dashboards
- **Account Team View:** Sales data filtered by parent account with vendor breakdown
- **Partner Team View:** Vendor sales aggregated by classified accounts
- **Executive Roll-up View:** High-level KPIs across account hierarchies

### Data Visualization
- Charts and graphs for sales trends over time
- Interactive drill-down capabilities
- Responsive design for desktop and mobile

## Technology Stack
- **React 18** with TypeScript
- **Vite** for build tooling and dev server
- **Axios** for API communication
- **Chart.js/Recharts** for data visualization
- **Tailwind CSS** for styling (planned)

## Development
- Hot reload enabled for rapid development
- API requests proxied to FastAPI backend
- TypeScript for type safety
