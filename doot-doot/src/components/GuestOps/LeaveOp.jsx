import { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import RequestHandler from '../../utils/RequestHandler';

const LeaveOrDeleteOp = ({ room, goHome, user }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);

  const isOwner = room.owner.username === user.username;

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
            .then(goHome)
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
          {!isOwner && 'Leave'}
          {isOwner && 'Delete'}
        </Button>
      </Form>
    </div>
  );
};

export default LeaveOrDeleteOp;
