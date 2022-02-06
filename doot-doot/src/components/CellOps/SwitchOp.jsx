import { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import RequestHandler from '../../utils/RequestHandler';

const SwitchOp = ({ room, cell }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);

  return (
    <div>
      <p className="lead">
        Switch State
      </p>

      <Form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/switch/${room.id}/`, 'post', { x: cell.x, y: cell.y })
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
        <Button loading={loading} disabled={loading} variant="primary" type="submit">Switch</Button>
      </Form>
    </div>
  );
};

export default SwitchOp;
