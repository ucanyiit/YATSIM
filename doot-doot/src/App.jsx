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
  const [sim, setSim] = useState(null);
  const [cells, setCells] = useState(null);
  const [users, setUsers] = useState(null);
  const [room, setRoom] = useState(null);
  const [trains, setTrains] = useState(null);
  const webSocket = useRef(null);
  const [dashboard, setDashboard] = useState(null);

  const loadDashboard = () => {
    setLoading(true);
    (new RequestHandler()).request('dashboard', 'get')
      .then((response) => {
        setDashboard(response);
      })
      .catch(() => setFailed(true))
      .finally(() => setLoading(false));
  };

  if (!loading && !failedToLoad && !dashboard && page === 'home') {
    loadDashboard();
  }

  useEffect(() => {
    setFailed(false);
    setLoading(false);
    if (page === 'home') {
      loadDashboard();
    }
    if (page !== 'room') {
      if (webSocket.current) { webSocket.current.close(); }
      return;
    }
    const connectionString = `ws://localhost:8000/ws/play/${room.id}/${token}`;
    webSocket.current = new WebSocket(connectionString);
    webSocket.current.onmessage = (evt) => {
      const message = JSON.parse(evt.data);
      const {
        event,
        cells: inc_cells,
        users: inc_users,
        trains: inc_trains,
        guests,
        sim: inc_sim,
      } = message;
      switch (event) {
        case 'cell_change':
          setCells(inc_cells);
          break;
        case 'users':
          setUsers(inc_users);
          setRoom({ ...room, guests });
          break;
        case 'trains':
          setTrains(inc_trains);
          break;
        case 'sim_update':
          setSim(inc_sim);
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
  }, [page]);

  const goHome = () => {
    setPage('home');
    setRoom(null);
    setCells(null);
    setUsers(null);
    setSim(null);
    setTrains(null);
  };

  const setRoomData = (roomId) => {
    setLoading(true);
    (new RequestHandler()).request(`room/${roomId}`, 'get')
      .then((response) => {
        setSim(response.sim);
        setRoom(response.room);
        setTrains(response.trains);
        setUsers(response.users);
        setCells(response.cells);
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
      <Dashboard goRoom={setRoomData} dashboard={dashboard} />
      )}
      {page === 'room' && (
      <Room
        user={dashboard.user}
        goHome={goHome}
        roomData={{
          cells, users, room, trains, sim,
        }}
      />
      )}
      {page === 'create' && <CreateRoom goHome={goHome} />}
    </Container>
  );
};

export default App;
