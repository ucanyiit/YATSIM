import { useState } from 'react';
import axios from 'axios';
import { Button, Form } from 'react-bootstrap';

const CreateRoom = () => {
  const [loading, setLoading] = useState(false);
  const [failedToLoad, setFailed] = useState(false);
  const [name, setName] = useState('');
  const [width, setWidth] = useState('');
  const [height, setHeight] = useState('');

  if (loading || failedToLoad) {
    return (
      <div>
        {failedToLoad && 'Failed to load'}
        {loading && 'Loading..'}
      </div>
    );
  }

  return (
    <div>
      <h2>
        Create Room
      </h2>
      <Form
        onSubmit={(e) => {
          e.preventDefault();
          console.log(height, width, name);
          setLoading(true);
          axios.get('http://localhost:8000/dashboard')
            .then((response) => {
              console.log('yes', response);
            })
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <Form.Group className="mb-3" controlId="name">
          <Form.Label>Room Name</Form.Label>
          <Form.Control type="text" placeholder="Name" onChange={(e) => setName(e.target.value)} required />
        </Form.Group>

        <Form.Group className="mb-3" controlId="width">
          <Form.Label>Width</Form.Label>
          <Form.Control type="number" placeholder="Width" onChange={(e) => setWidth(e.target.value)} min={1} max={100} required />
        </Form.Group>

        <Form.Group className="mb-3" controlId="height">
          <Form.Label>Height</Form.Label>
          <Form.Control type="number" placeholder="Height" onChange={(e) => setHeight(e.target.value)} min={1} max={100} required />
        </Form.Group>

        <Button variant="primary" type="submit">
          Create
        </Button>
      </Form>
    </div>
  );
};

export default CreateRoom;
