import {
  Button,
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography,
} from '@mui/material';

const RoomRow = ({ room, goRoom }) => (
  <TableRow
    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
  >
    <TableCell component="th" scope="row">
      {room.id}
    </TableCell>
    <TableCell>{room.room_name}</TableCell>
    <TableCell>{room.owner.username}</TableCell>
    <TableCell><Button onClick={() => goRoom(room.id)}>Enter</Button></TableCell>
  </TableRow>
);

const Dashboard = ({ goRoom, dashboard }) => (
  <div>
    <Typography variant="h4" component="h1" mt={2} mb={2}>
      Home
    </Typography>
    <Typography variant="subtitle1" component="h2" mt={2} mb={2}>
      {`You are logged in as ${dashboard.user.username}.`}
    </Typography>
    <TableContainer>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Name</TableCell>
            <TableCell>Owner</TableCell>
            <TableCell />
          </TableRow>
        </TableHead>
        <TableBody>
          {dashboard.owned_rooms.map((room) => (
            <RoomRow key={room.id} room={room} goRoom={goRoom} />))}
          {dashboard.guest_rooms.map((room) => (
            <RoomRow key={room.id} room={room} goRoom={goRoom} />))}
        </TableBody>
      </Table>
    </TableContainer>
  </div>
);

export default Dashboard;
