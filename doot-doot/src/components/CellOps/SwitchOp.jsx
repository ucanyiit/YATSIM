import { Button, Typography } from '@mui/material';
import { useState } from 'react';
import RequestHandler from '../../utils/RequestHandler';

const SwitchOp = ({ room, cell }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);

  return (
    <div>
      <Typography variant="subtitle1" component="h6" mt={1} mb={1}>
        Switch State
      </Typography>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/switch/`, 'post', { x: cell.x, y: cell.y })
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
        <Button size="small" loading={loading} disabled={loading} variant="contained" type="submit">Switch</Button>
      </form>
    </div>
  );
};

export default SwitchOp;
