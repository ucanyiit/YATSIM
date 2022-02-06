import { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import RequestHandler from '../../utils/RequestHandler';

const RemoveGuestOp = ({ room }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [guest, setGuest] = useState(room.guests[0]?.username);

  return (
    <div>
      <p className="lead">
        Remove
      </p>

      <Form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/user/`, 'delete', { username: guest })
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
            {room.guests.map((cur_guest) => (
              <option key={cur_guest.username} value={cur_guest.username}>
                {cur_guest.username}
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
          Remove
        </Button>
      </Form>
    </div>
  );
};

export default RemoveGuestOp;
