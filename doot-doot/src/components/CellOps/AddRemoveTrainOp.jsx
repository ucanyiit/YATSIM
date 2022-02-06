import { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import RequestHandler from '../../utils/RequestHandler';

const types = [
  { value: '0', name: 'Mitsky' },
  { value: '1', name: 'Lady Gaga' },
];

const AddRemoveTrainOp = ({ room, cell }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [type, setType] = useState(cell.type);

  if (cell.train) {
    return (
      <div>
        <p className="lead">
          Remove Train
        </p>

        <Form
          onSubmit={(e) => {
            e.preventDefault();
            setLoading(true);
            (new RequestHandler()).request(`room/remove_train/${room.id}/`, 'post', { train_id: cell.train.id })
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
          (new RequestHandler()).request(`room/add_train/${room.id}/`, 'post', { x: cell.x, y: cell.y, type })
            .then(() => {})
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <Form.Group className="mb-3" controlId="type">
          <Form.Label>Type</Form.Label>
          <Form.Select value={cell.type} onChange={(e) => setType(e.target.value)}>
            {types.map((train_type) => (
              <option key={train_type.value} value={train_type.value}>
                {train_type.name}
              </option>
            ))}
          </Form.Select>
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
