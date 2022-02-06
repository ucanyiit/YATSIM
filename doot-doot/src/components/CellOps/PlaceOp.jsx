import { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import RequestHandler from '../../utils/RequestHandler';

const types = [
  { value: '0', name: 'Blank' },
  { value: '1', name: 'Straight' },
  { value: '2', name: 'Curved' },
  { value: '3', name: 'Y Junction' },
  { value: '4', name: 'Y Junction Mirrored' },
  { value: '5', name: 'X Junction' },
  { value: '6', name: 'Cross Roads' },
  { value: '7', name: 'Cross Bridge' },
  { value: '8', name: 'Station' },
];

const PlaceOp = ({ room, cell }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [type, setType] = useState(cell.type);

  return (
    <div>
      <p className="lead">
        Place
      </p>

      <Form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/place/`, 'post', { x: cell.x, y: cell.y, type })
            .then(() => {})
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <Form.Group className="mb-3" controlId="type">
          <Form.Label>Type</Form.Label>
          <Form.Select
            value={type}
            onChange={(e) => setType(e.target.value)}
            required
          >
            {types.map((cell_type) => (
              <option key={cell_type.value} value={cell_type.value}>
                {cell_type.name}
              </option>
            ))}
          </Form.Select>
        </Form.Group>
        {failed && (
          <p>
            Failed request.
          </p>
        )}
        <Button loading={loading} disabled={loading} variant="primary" type="submit">Place</Button>
      </Form>
    </div>
  );
};

export default PlaceOp;
