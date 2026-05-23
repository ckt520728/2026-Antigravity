import React from 'react';
import ReactDOM from 'react-dom/client';
import App from '../ode.tsx'; // Import the main robust app we built
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
