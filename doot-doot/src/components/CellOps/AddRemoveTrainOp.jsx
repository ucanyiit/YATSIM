import { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import RequestHandler from '../../utils/RequestHandler';

const types = [
  { value: '0', name: 'Mitski' },
  { value: '1', name: 'Lady Gaga' },
];

const AddRemoveTrainOp = ({ room, cell }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [type, setType] = useState(cell.train?.type || 0);
  const [length, setLength] = useState(1);
  const type_name = cell.train?.type === 1 ? 'Lady Gaga' : 'Mitski';

  if (cell.train) {
    return (
      <div>
        <p className="lead">
          {`Remove ${type_name}`}
        </p>

        <Form
          onSubmit={(e) => {
            e.preventDefault();
            setLoading(true);
            (new RequestHandler()).request(`room/${room.id}/train`, 'delete', { train_id: cell.train.id })
              .then(() => {})
              .catch(() => setFailed(true))
              .finally(() => setLoading(false));
          }}
        >
          {failed && (
            <p>
              Failed request.
            </p>
          )}
          <Button loading={loading} disabled={loading} variant="primary" type="submit">Remove</Button>
        </Form>
      </div>
    );
  }
  return (
    <div>
      <p className="lead">
        Add Train
      </p>

      <Form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/train/`, 'post', { source: { x: cell.x, y: cell.y }, type, length })
            .then(() => {})
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <Form.Group className="mb-3" controlId="type">
          <Form.Label>Type</Form.Label>
          <Form.Select className="mb-3" value={type} onChange={(e) => setType(e.target.value)}>
            {types.map((train_type) => (
              <option key={train_type.value} value={train_type.value}>
                {train_type.name}
              </option>
            ))}
          </Form.Select>
          <Form.Group className="mb-3" controlId="length">
            <Form.Label>Length</Form.Label>
            <Form.Control type="number" placeholder="Length" onChange={(e) => setLength(e.target.value)} min={1} max={20} required />
          </Form.Group>
        </Form.Group>
        {failed && (
          <p>
            Failed request.
          </p>
        )}
        <Button loading={loading} disabled={loading} variant="primary" type="submit">Add</Button>
      </Form>
    </div>
  );
};

export default AddRemoveTrainOp;
