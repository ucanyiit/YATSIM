import { useState } from 'react';
import { OverlayTrigger, Popover } from 'react-bootstrap';
import CellOps from '../components/CellOps';
import './room.css';
import { getCellImage, getWagonImage } from './RoomHelper';

const Room = ({ roomData: { room, cells, trains } }) => {
  const running = false;
  const [grid, setMap] = useState(null);

  const newGrid = [];
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
    newGrid.push(row);
  }

  // eslint-disable-next-line no-restricted-syntax
  for (const train of trains) {
    console.log(train);
    // eslint-disable-next-line no-restricted-syntax
    for (const wagon of train.wagon_set) {
      newGrid[wagon.y][wagon.x].wagons.push({ type: train.type, direction: wagon.direction });
    }
  }

  if (JSON.stringify(grid) !== JSON.stringify(newGrid)) {
    setMap(newGrid);
  }

  if (!grid) {
    return (
      <div>
        Loading...
      </div>
    );
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
        {`/${room.room_name}, height: ${room.height}, width: ${room.width}, ${running && 'Simulation is running 🚀'}${!running && 'Simulation is stopped 🌱'}`}
      </h5>
      <div>
        Guests:
        {room.guests.map((u) => (
          <span>
            {u.username}
          </span>
        ))}
      </div>
      <center>
        <table>
          {grid.map((row) => (
            <tr>
              {row.map((cell) => (
                <td>
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
        </table>
      </center>
    </div>
  );
};

export default Room;
