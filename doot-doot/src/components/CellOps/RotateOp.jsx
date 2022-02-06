import { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import RequestHandler from '../../utils/RequestHandler';

const directions = [
  { value: '0', name: 'NORTH' },
  { value: '1', name: 'EAST' },
  { value: '2', name: 'SOUTH' },
  { value: '3', name: 'WEST' },
];

const RotateOp = ({ room, cell }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [direction, setDirection] = useState(cell.direction);

  return (
    <div>
      <p className="lead">
        Rotate
      </p>

      <Form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/rotate/`, 'post', { x: cell.x, y: cell.y, direction })
            .then(() => {})
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <Form.Group className="mb-3" controlId="direction">
          <Form.Label>Direction</Form.Label>
          <Form.Select
            value={direction}
            onChange={(e) => setDirection(e.target.value)}
            required
          >
            {directions.map((cell_direction) => (
              <option key={cell_direction.value} value={cell_direction.value}>
                {cell_direction.name}
              </option>
            ))}
          </Form.Select>
        </Form.Group>
        {failed && (
          <p>
            Failed request.
          </p>
        )}
        <Button loading={loading} disabled={loading} variant="primary" type="submit">Rotate</Button>
      </Form>
    </div>
  );
};

export default RotateOp;
