import { useState } from 'react';
import { Button, Container } from 'react-bootstrap';
import CreateRoom from './pages/CreateRoom';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Room from './pages/Room';

const App = () => {
  const [page, setPage] = useState('home');
  const [roomId, setRoomId] = useState('');
  const [socket, setSocket] = useState(null);
  const token = localStorage.getItem('token');

  if (!socket) {
    console.log('enter', socket);
    const ws = new WebSocket('ws://localhost:8000/');
    setSocket(ws);
    console.log('done', socket);

    ws.onopen = () => {
      // on connecting, do nothing but log it to the console
      console.log('connected', ws.url, ws.readyState, ws);
    };

    ws.onmessage = (evt) => {
      // listen to data sent from the websocket server
      // const message = JSON.parse(evt.data);
      console.log(evt.data);
    };

    ws.onclose = () => {
      console.log('disconnected');
      // automatically try to reconnect on connection loss
    };
  }

  return (
    <Container className="mt-3">
      <div className="mb-3">
        <Button className="me-2" onClick={() => setPage('home')}>
          Home
        </Button>
        <Button className="me-2" onClick={() => setPage('create')}>
          Create Room
        </Button>
        {!token && (
        <Button onClick={() => setPage('login')}>
          Login
        </Button>
        )}
        {token && (
          <Button onClick={() => {
            localStorage.removeItem('token');
            window.location.reload(false);
          }}
          >
            Logout
          </Button>
        )}
      </div>
      {page === 'home' && (
      <Dashboard goRoom={(room_id) => {
        setPage('room');
        setRoomId(room_id);
      }}
      />
      )}
      {page === 'room' && <Room id={roomId} />}
      {page === 'create' && <CreateRoom id={roomId} goHome={() => setPage('home')} />}
      {page === 'login' && <Login goHome={() => setPage('home')} />}
      <Button onClick={() => {
        socket.send('ping');
      }}
      >
        Ping
      </Button>
    </Container>
  );
};

export default App;
