import { useState } from 'react';
import { Container } from 'react-bootstrap';
import Header from './components/Header';
import CreateRoom from './pages/CreateRoom';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Room from './pages/Room';
import RequestHandler from './utils/RequestHandler';

const App = () => {
  const token = localStorage.getItem('token');
  const [page, setPage] = useState('home');
  const [loading, setLoading] = useState(false);
  const [failedToLoad, setFailed] = useState(false);
  const [roomData, setRoomData] = useState(null);

  const goHome = () => {
    setPage('home');
    setRoomData(null);
  };

  const setRoom = (roomId) => {
    setLoading(true);
    (new RequestHandler()).request(`room/${roomId}`, 'get')
      .then((response) => {
        setRoomData(response);
        setPage('room');
      })
      .catch(() => setFailed(true))
      .finally(() => setLoading(false));
  };

  if (loading || failedToLoad) {
    return (
      <Container className="mt-3">
        <Header token={token} setPage={setPage} />
        {failedToLoad && 'Failed to load, please refresh.'}
        {loading && 'Loading..'}
      </Container>
    );
  }

  if (!token) {
    return (
      <Container className="mt-3">
        <Header token={token} setPage={setPage} />
        {page === 'login' && <Login goHome={goHome} />}
        {page !== 'login' && <p>Please login to see dashboard.</p>}
      </Container>
    );
  }

  return (
    <Container className="mt-3">
      <Header token={token} setPage={setPage} />
      {page === 'home' && (
      <Dashboard goRoom={setRoom} />
      )}
      {page === 'room' && <Room goHome={goHome} roomData={roomData} />}
      {page === 'create' && <CreateRoom goHome={goHome} />}
    </Container>
  );
};

export default App;
