import { Container, Row } from 'react-bootstrap';
import CloneOp from '../CloneOp';
import AddGuestOp from './AddGuestOp';
import LeaveOp from './LeaveOp';
import RemoveGuestOp from './RemoveGuestOp';

const GuestOps = ({ room, users }) => (
  <Container>
    <h4>
      Cell Operations
    </h4>
    <Row className="my-2">
      <LeaveOp room={room} />
    </Row>
    <Row className="my-2">
      <RemoveGuestOp room={room} />
    </Row>
    <Row className="my-2">
      <AddGuestOp room={room} users={users} />
    </Row>
    <Row className="my-2">
      <CloneOp room={room} />
    </Row>
  </Container>
);

export default GuestOps;
