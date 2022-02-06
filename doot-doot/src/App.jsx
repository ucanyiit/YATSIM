import { useState } from 'react';
import { Button, Container } from 'react-bootstrap';
import Header from './components/Header';
import CreateRoom from './pages/CreateRoom';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Room from './pages/Room';
import RequestHandler from './utils/RequestHandler';

const App = () => {
  const [page, setPage] = useState('home');
  const [socket, setSocket] = useState(null);
  const token = localStorage.getItem('token');
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

  if (!socket) {
    console.log('enter', socket);
    const ws = new WebSocket('ws://localhost:8000/');
    setSocket(ws);
    console.log('done', socket);

    ws.onopen = () => {
      console.log('connected', ws.url, ws.readyState, ws);
    };

    ws.onmessage = (evt) => {
      const message = JSON.parse(evt.data);
      console.log(message);
    };

    ws.onclose = () => {
      console.log('disconnected');
    };
  }

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
      {token && (
      <Button onClick={() => {
        socket.send(JSON.stringify({ type: 'attach', token, room_id: 2 }));
      }}
      >
        Ping
      </Button>
      )}
    </Container>
  );
};

export default App;
