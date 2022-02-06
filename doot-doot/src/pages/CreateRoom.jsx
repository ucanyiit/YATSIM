import { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import RequestHandler from '../utils/RequestHandler';

const CreateRoom = ({ goHome }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [room_name, setRoomName] = useState('');
  const [width, setWidth] = useState('');
  const [height, setHeight] = useState('');

  return (
    <div>
      <h2>
        Create Room
      </h2>
      <Form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request('create_room/', 'post', { height, width, room_name })
            .then(goHome)
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <Form.Group className="mb-3" controlId="name">
          <Form.Label>Room Name</Form.Label>
          <Form.Control type="text" placeholder="Name" onChange={(e) => setRoomName(e.target.value)} required maxLength={150} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="width">
          <Form.Label>Width</Form.Label>
          <Form.Control type="number" placeholder="Width" onChange={(e) => setWidth(e.target.value)} min={2} max={16} required />
        </Form.Group>

        <Form.Group className="mb-3" controlId="height">
          <Form.Label>Height</Form.Label>
          <Form.Control type="number" placeholder="Height" onChange={(e) => setHeight(e.target.value)} min={2} max={16} required />
        </Form.Group>
        {failed && (
        <p>
          Failed to create a room.
        </p>
        )}
        <Button loading={loading} disabled={loading} variant="primary" type="submit">
          Create
        </Button>
      </Form>
    </div>
  );
};

export default CreateRoom;
