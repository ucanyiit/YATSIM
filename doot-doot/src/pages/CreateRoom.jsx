import {
  Button, FormGroup, TextField, Typography,
} from '@mui/material';
import { useState } from 'react';
import RequestHandler from '../utils/RequestHandler';

const CreateRoom = ({ goHome }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [room_name, setRoomName] = useState('');
  const [width, setWidth] = useState('');
  const [height, setHeight] = useState('');

  return (
    <div>
      <Typography variant="h4" component="h1" mt={2} mb={2}>
        Create Room
      </Typography>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request('create_room/', 'post', { height, width, room_name })
            .then(goHome)
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <FormGroup sx={{ mb: 2 }}>
          <TextField label="Room Name" type="text" placeholder="Name" onChange={(e) => setRoomName(e.target.value)} required maxLength={150} />
        </FormGroup>

        <FormGroup sx={{ mb: 2 }}>
          <TextField label="Width" type="number" placeholder="Width" onChange={(e) => setWidth(e.target.value)} min={2} max={16} required />
        </FormGroup>

        <FormGroup sx={{ mb: 2 }}>
          <TextField label="Height" type="number" placeholder="Height" onChange={(e) => setHeight(e.target.value)} min={2} max={16} required />
        </FormGroup>
        {failed && (
        <p>
          Failed to create a room.
        </p>
        )}
        <Button loading={loading} disabled={loading} variant="contained" type="submit">
          Create
        </Button>
      </form>
    </div>
  );
};

export default CreateRoom;
