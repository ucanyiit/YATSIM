import { Button, ListGroup } from 'react-bootstrap';

const Dashboard = ({ goRoom, dashboard }) => (
  <div>
    <h2>
      Home
    </h2>
    <span>
      {`You are logged in as ${dashboard.user.username}.`}
    </span>
    <ListGroup>
      {dashboard.owned_rooms.map((room) => (
        <ListGroup.Item key={room.id}>
          {`${room.id}: `}
          <b>{room.owner.username}</b>
          {`/${room.room_name}, `}
          <Button onClick={() => goRoom(room.id)}>go</Button>
        </ListGroup.Item>
      ))}
      {dashboard.guest_rooms.map((room) => (
        <ListGroup.Item key={room.id}>
          {`${room.id}: ${room.owner.username}/${room.room_name}, `}
          <Button onClick={() => goRoom(room.id)}>go</Button>
        </ListGroup.Item>
      ))}
    </ListGroup>
  </div>
);

export default Dashboard;
