import { useState } from 'react';
import { Button, Container } from 'react-bootstrap';
import CreateRoom from './pages/CreateRoom';
import Dashboard from './pages/Dashboard';
import Room from './pages/Room';

const App = () => {
  const [page, setPage] = useState('home');
  const [roomId, setRoomId] = useState('');
  const [socket, setSocket] = useState(null);

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
        <Button onClick={() => setPage('home')} className="me-2">
          Home
        </Button>
        <Button onClick={() => setPage('create')}>
          Create Room
        </Button>
      </div>
      {page === 'home' && (
      <Dashboard goRoom={(room_id) => {
        setPage('room');
        setRoomId(room_id);
      }}
      />
      )}
      {page === 'room' && <Room id={roomId} />}
      {page === 'create' && <CreateRoom id={roomId} />}
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
