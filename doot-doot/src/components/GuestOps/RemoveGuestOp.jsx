import {
  Button, FormGroup, MenuItem, Select, Typography,
} from '@mui/material';
import { useState } from 'react';
import RequestHandler from '../../utils/RequestHandler';

const RemoveGuestOp = ({ room }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [guest, setGuest] = useState(room.guests[0]?.username);

  return (
    <div>
      <Typography variant="subtitle1" component="h6" mt={1} mb={1}>
        Remove User
      </Typography>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/user/`, 'delete', { username: guest })
            .then(() => {})
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <FormGroup sx={{ mb: 2 }}>
          <Select
            label="Guest"
            value={guest}
            onChange={(e) => setGuest(e.target.value)}
            required
          >
            {room.guests.map((cur_guest) => (
              <MenuItem key={cur_guest.username} value={cur_guest.username}>
                {cur_guest.username}
              </MenuItem>
            ))}
          </Select>
        </FormGroup>
        {failed && (
          <p>
            Failed request.
          </p>
        )}
        <Button loading={loading} disabled={loading} variant="contained" type="submit">
          Remove
        </Button>
      </form>
    </div>
  );
};

export default RemoveGuestOp;
