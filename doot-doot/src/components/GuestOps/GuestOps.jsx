import { Container, Row } from 'react-bootstrap';
import CloneOp from '../CloneOp';
import AddGuestOp from './AddGuestOp';
import LeaveOp from './LeaveOp';
import RemoveGuestOp from './RemoveGuestOp';

const GuestOps = ({
  room, users, goHome, user,
}) => (
  <Container>
    <h4>
      User Operations
    </h4>
    <Row className="my-2">
      <LeaveOp room={room} goHome={goHome} user={user} />
    </Row>
    <Row className="my-2">
      <RemoveGuestOp room={room} />
    </Row>
    <Row className="my-2">
      <AddGuestOp room={room} users={users} />
    </Row>
    <Row className="my-2">
      <CloneOp room={room} goHome={goHome} />
    </Row>
  </Container>
);

export default GuestOps;
