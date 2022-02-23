import { Button, Typography } from '@mui/material';
import { useState } from 'react';
import RequestHandler from '../../utils/RequestHandler';

const ToggleOp = ({ room, running }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);

  return (
    <div>
      <Typography variant="subtitle1" component="h6" mt={1} mb={1}>
        Toggle Simulation
      </Typography>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/toggle/`, 'post', {})
            .then()
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
          {!running && 'Continue'}
          {running && 'Stop'}
        </Button>
      </form>
    </div>
  );
};

export default ToggleOp;
