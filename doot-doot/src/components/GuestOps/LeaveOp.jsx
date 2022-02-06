import { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import RequestHandler from '../../utils/RequestHandler';

const LeaveOrDeleteOp = ({ room }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);

  return (
    <div>
      <p className="lead">
        Leave
      </p>

      <Form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/leave/`, 'post', { })
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
        <Button loading={loading} disabled={loading} variant="primary" type="submit">
          Leave
        </Button>
      </Form>
    </div>
  );
};

export default LeaveOrDeleteOp;
