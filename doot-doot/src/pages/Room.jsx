import { OverlayTrigger, Popover } from 'react-bootstrap';
import CellOps from '../components/CellOps/CellOps';
import GuestOps from '../components/GuestOps/GuestOps';
import './room.css';
import { getCellImage, getWagonImage } from './RoomHelper';

const Room = ({
  roomData: {
    room, cells, trains, users,
  },
}) => {
  let running = false;

  const grid = [];
  const newCells = cells.sort((a, b) => {
    if (a.y < b.y) return -1;
    if (a.y > b.y) return 1;
    return a.x < b.x ? -1 : 1;
  });

  // eslint-disable-next-line no-restricted-syntax
  for (let i = 0; i < room.height; i += 1) {
    const row = [];
    for (let j = 0; j < room.width; j += 1) {
      row.push({ ...newCells[i * room.width + j], wagons: [] });
    }
    grid.push(row);
  }

  // eslint-disable-next-line no-restricted-syntax
  for (const train of trains) {
    // eslint-disable-next-line no-restricted-syntax
    for (const wagon of train.wagon_set) {
      running = true;
      grid[wagon.y][wagon.x].wagons.push({ type: train.type, direction: wagon.direction });
    }
    grid[train.source.y][train.source.x].train = train;
  }

  const popover = (cell) => (
    <Popover id="popover-basic">
      <Popover.Body>
        <CellOps cell={cell} room={room} />
      </Popover.Body>
    </Popover>
  );

  return (
    <div>
      <h5>
        {`${room.id}: `}
        <b>{room.owner.username}</b>
        {`/${room.room_name}, height: ${room.height}, width: ${room.width}, `}
        {running && 'Simulation is running 🚀'}
        {!running && 'Simulation is stopped 🌱'}
      </h5>
      <div>
        Guests:
        {room.guests.map((u) => (
          <span key={u}>
            {`${u.username}, `}
          </span>
        ))}
        {room.guests.length === 0 && (
        <span>
          {' No guests :('}
        </span>
        )}
      </div>
      <center>
        <table>
          <tbody>
            {grid.map((row) => (
              <tr key={row[0].y}>
                {row.map((cell) => (
                  <td key={cell.x}>
                    <OverlayTrigger trigger="click" placement="right" overlay={popover(cell)}>
                      <div className="cell">
                        <img
                          alt="wow"
                          className={`direction${cell.direction}`}
                          width="48"
                          height="48"
                          src={getCellImage(cell.type, cell.state)}
                        />
                        {cell.wagons.map((wagon) => (
                          <img
                            key={`${wagon.type}`}
                            alt="doot-doot"
                            className={`train direction${wagon.direction}`}
                            width="48"
                            height="48"
                            src={getWagonImage(wagon.type)}
                          />
                        ))}
                      </div>
                    </OverlayTrigger>

                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </center>
      <GuestOps room={room} users={users} />
    </div>
  );
};

export default Room;
