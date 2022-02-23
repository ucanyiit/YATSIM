import { useState } from 'react';
import {
  Button, FormGroup, TextField, Typography,
} from '@mui/material';
import RequestHandler from '../utils/RequestHandler';

const CloneOp = ({ room, goHome }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [roomName, setRoomName] = useState('');

  return (
    <div>
      <Typography variant="subtitle1" component="h6" mt={1} mb={1}>
        Clone
      </Typography>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/clone/`, 'post', { room_name: roomName })
            .then(goHome)
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <FormGroup sx={{ mb: 2 }}>
          <TextField type="text" label="Room Name" onChange={(e) => setRoomName(e.target.value)} required />
          {failed && (
          <p>
            Failed request.
          </p>
          )}
        </FormGroup>
        <Button variant="contained" loading={loading} disabled={loading} type="submit">
          Clone
        </Button>
      </form>
    </div>
  );
};

export default CloneOp;
