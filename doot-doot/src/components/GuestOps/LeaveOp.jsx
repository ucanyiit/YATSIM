import { Button, Typography } from '@mui/material';
import { useState } from 'react';
import RequestHandler from '../../utils/RequestHandler';

const LeaveOrDeleteOp = ({ room, goHome, user }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);

  const isOwner = room.owner.username === user.username;

  return (
    <div>
      <Typography variant="subtitle1" component="h6" mt={1} mb={1}>
        Leave Room
      </Typography>

      <form
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
        <Button loading={loading} disabled={loading} variant="contained" type="submit">
          {!isOwner && 'Leave'}
          {isOwner && 'Delete'}
        </Button>
      </form>
    </div>
  );
};

export default LeaveOrDeleteOp;
