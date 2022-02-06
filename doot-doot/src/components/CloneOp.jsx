import { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import RequestHandler from '../utils/RequestHandler';

const CloneOp = ({ room }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [roomName, setRoomName] = useState('');

  return (
    <div>
      <p className="lead">
        Clone
      </p>

      <Form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/clone/`, 'post', { room_name: roomName })
            .then(() => {})
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <Form.Group className="mb-3" controlId="name">
          <Form.Label>Room Name</Form.Label>
          <Form.Control type="text" placeholder="Room Name" onChange={(e) => setRoomName(e.target.value)} required />
        </Form.Group>
        {failed && (
          <p>
            Failed request.
          </p>
        )}
        <Button loading={loading} disabled={loading} variant="primary" type="submit">
          Clone
        </Button>
      </Form>
    </div>
  );
};

export default CloneOp;
