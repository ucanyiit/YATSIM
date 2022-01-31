import { useState } from 'react';
import Dashboard from './pages/Dashboard';

const App = () => {
  const [page, setPage] = useState('home');

  return (
    <div className="App">
      <p>
        Edit
      </p>
      <button type="button" onClick={() => setPage('home')}>
        hi
      </button>
      {page === 'home' && <Dashboard />}
    </div>
  );
};

export default App;
