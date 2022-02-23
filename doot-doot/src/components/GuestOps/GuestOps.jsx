import { Container, Grid, Typography } from '@mui/material';
import CloneOp from '../CloneOp';
import AddGuestOp from './AddGuestOp';
import LeaveOp from './LeaveOp';
import RemoveGuestOp from './RemoveGuestOp';

const GuestOps = ({
  room, users, goHome, user,
}) => (
  <Container>
    <Typography mt={2} variant="h5" component="h5">
      User Operations
    </Typography>
    <Grid
      container
      spacing={2}
      direction="row"
      justifyContent="center"
    >
      <Grid item xs={6} md={3}>
        <AddGuestOp room={room} users={users} />
      </Grid>
      <Grid item xs={6} md={3}>
        <RemoveGuestOp room={room} />
      </Grid>
      <Grid item xs={6} md={3}>
        <CloneOp room={room} goHome={goHome} />
      </Grid>
      <Grid item xs={6} md={3}>
        <LeaveOp room={room} goHome={goHome} user={user} />
      </Grid>
    </Grid>
  </Container>
);

export default GuestOps;
