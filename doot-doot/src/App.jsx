/* eslint-disable no-case-declarations */
import { useEffect, useRef, useState } from 'react';
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
  const [room_id, set_room_id] = useState(null);
  const [roomData, setRoomData] = useState(null);
  const webSocket = useRef(null);

  useEffect(() => {
    if (!room_id) return;
    const connectionString = `ws://localhost:8000/ws/play/${room_id}/${token}`;
    webSocket.current = new WebSocket(connectionString);
    webSocket.current.onmessage = (evt) => {
      const message = JSON.parse(evt.data);
      const { event } = message;
      switch (event) {
        case 'cell_change':
          const { cell } = message;
          const { cells } = roomData;
          cells[cell.y * roomData.room.width + cell.x] = cell;
          setRoomData({
            ...roomData,
            cells,
          });
          break;
        default:
      }
    };
    webSocket.current.onopen = () => {
      console.log('connected');
    };
    webSocket.current.onclose = () => {
      console.log('disconnected');
    };
  }, [room_id]);

  const goHome = () => {
    setPage('home');
    setRoomData(null);
  };

  const setRoom = (roomId) => {
    setLoading(true);
    (new RequestHandler()).request(`room/${roomId}`, 'get')
      .then((response) => {
        setRoomData(response);
        set_room_id(response.room.id);
        setPage('room');
      })
      .catch((e) => {
        console.error(e);
        setFailed(true);
      })
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
