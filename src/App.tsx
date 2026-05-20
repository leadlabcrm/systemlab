import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import SopRenderer from './components/SopRenderer';
import './App.css';

const navItems = [
  { id: 'sales', label: 'Sales & Closing', sops: ['inbound-qualification', 'discovery-call', 'proposal-generation'] },
  { id: 'seo', label: 'SEO Operations', sops: ['keyword-research', 'on-page-audit', 'backlink-outreach'] },
  { id: 'marketing', label: 'Marketing', sops: ['content-publishing', 'social-media-sop'] },
  { id: 'operations', label: 'Operations', sops: ['client-onboarding', 'monthly-reporting'] },
];

function Sidebar() {
  const location = useLocation();

  return (
    <aside className="sidebar">
      <div className="brand">
        <em>system</em><strong>lab.</strong>
      </div>
      
      <div className="nav-section">
        <div className="nav-label">LIBRARY</div>
        <nav>
          {navItems.map(category => {
            const isActive = location.pathname.includes(`/category/${category.id}`);
            return (
              <div key={category.id} className="nav-category">
                <Link to={`/category/${category.id}/${category.sops[0]}`} className={`nav-item ${isActive ? 'active' : ''}`}>
                  {category.label}
                </Link>
                {isActive && (
                  <div className="sub-nav">
                    {category.sops.map(sop => (
                      <Link 
                        key={sop} 
                        to={`/category/${category.id}/${sop}`}
                        className={`sub-item ${location.pathname.endsWith(sop) ? 'active' : ''}`}
                      >
                        {sop.replace(/-/g, ' ')}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}

function Dashboard() {
  return (
    <div className="empty-state">
      <h2>SYSTEMLAB</h2>
      <p>Select a category from the sidebar to view or edit standard operating procedures.</p>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <div className="app-layout">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/category/:categoryId/:sopId" element={<SopRenderer />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
