import { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import RequestHandler from '../../utils/RequestHandler';

const AddGuestOp = ({ room, users }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [guest, setGuest] = useState(users[0]?.username);

  return (
    <div>
      <p className="lead">
        Add
      </p>

      <Form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/user/`, 'post', { username: guest })
            .then(() => {})
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <Form.Group className="mb-3" controlId="guest">
          <Form.Label>Guest</Form.Label>
          <Form.Select
            value={guest}
            onChange={(e) => setGuest(e.target.value)}
            required
          >
            {users.map((user) => (
              <option key={user.username} value={user.username}>
                {user.username}
              </option>
            ))}
          </Form.Select>
        </Form.Group>
        {failed && (
          <p>
            Failed request.
          </p>
        )}
        <Button loading={loading} disabled={loading} variant="primary" type="submit">
          Add
        </Button>
      </Form>
    </div>
  );
};

export default AddGuestOp;
