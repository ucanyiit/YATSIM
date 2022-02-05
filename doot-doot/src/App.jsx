import { useState } from 'react';
import { Button, Container } from 'react-bootstrap';
import CreateRoom from './pages/CreateRoom';
import Dashboard from './pages/Dashboard';
import Room from './pages/Room';

const App = () => {
  const [page, setPage] = useState('home');
  const [roomId, setRoomId] = useState('');

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
    </Container>
  );
};

export default App;
