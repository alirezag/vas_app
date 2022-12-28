
import './App.css';
import MyCard from './MyCard';
import {Card, Box, Button, CardHeader, CardMedia, InputLabel, MenuItem, FormControl} from '@mui/material'
import { useEffect, useState} from "react";
import listenerConfig from './speaker_list.json'
import Select, { SelectChangeEvent } from '@mui/material/Select';

function App() {

  const [data, setData] = useState([ 
    {
    title:   "habla comprensible",
    value : 0,
    mark : [{
      value: 0,
      label:'0 muy difícil de entender'
      } ,
      {
        value: 100,
        label: '100 muy fácil de entender'
      }]
    },
    {
      title:   "resonancia",
      value : 0,
      mark : [{
        value: 0,
        label:'0 extremadamente pobre/atípico'
        } ,
        {
          value: 100,
          label: '100 excelente/típico'
        }]
      },
      {
        title:   "precisión articulatoria",
        value : 0,
        mark : [{
          value: 0,
          label:'0 extremadamente pobre/atípico'
          } ,
          {
            value: 100,
            label: '100 excelente/típico'
          }]
        },
        {
          title:   "prosodia",
          value : 0,
          mark : [{
            value: 0,
            label:'0 extremadamente pobre/atípico'
            } ,
            {
              value: 100,
              label: '100 excelente/típico'
            }]
          },
          {
            title:   "calidad vocal​ ",
            value : 0,
            mark : [{
              value: 0,
              label:'0 extremadamente pobre/atípico'
              } ,
              {
                value: 100,
                label: '100 excelente/típico'
              }]
  }]);
  const [getValues,setValues] = useState([0,0,0,0,0]);
  const [getAll, setAll] = useState(null)
  const [playCount, setPlayCount ] = useState(0)
  const [listenerNumber, setListenerNumber] = useState(1)
  const onChange= (idx,v) => { 
    const vs = [...getValues];
    vs[idx]=v
    setValues(vs)
  }

  const handlelistenerNumberChange = (event: SelectChangeEvent) => { 
    setListenerNumber( event.target.value )
  }

  useEffect(() => { 
    setData( d => [...d])
  },[getAll])


  console.log(listenerConfig)


  return (
    <div className="App">
      <header className="App-header">
        VAS
        </header>
       <Box display="flex" justifyContent="center">
       <Card >
       <CardHeader
        action={
          <div> 
            <FormControl >
  <InputLabel id="demo-simple-select-label">Listener Number</InputLabel>
  <Select
    labelId="demo-simple-select-label"
    id="demo-simple-select"
    value={listenerNumber}
    label="Listener Number"
    onChange={handlelistenerNumberChange}
  >
    {listenerConfig.map( item => <MenuItem value={item.listener}>Listener {item.listener}</MenuItem>) }
    
  </Select>
</FormControl>
            <Button onClick={ (e) => document.getElementById("mymedia").play() }>Play</Button>
            <Button  onClick={ (ev) => { 
            if (getAll) {
              setAll([...getAll, getValues]);
            } else { 
              setAll([getValues]);
            }

            fetch(`/`, {
              method: 'POST', // or 'PUT'
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(getValues),
            })
              .then((response) => response.json())
              .then((data) => {
                console.log('Success:', data);
                setValues([0,0,0,0,0])
              })
              .catch((error) => {
                console.error('Error:', error);
              });
            }}>Save & Next</Button>
          </div>
      }
       />
        
        <CardMedia
        id="mymedia"
        component="audio"
        src="sounds/audio_sample.mp3"
        controls
        onPlay={(e) => {
          e.preventDefault()
          console.log(playCount)
          if (playCount===2) {
          //  e.preventDefault()
           console.log(e)
          //  e.target.stop()
        } else {
          setPlayCount( c => c+1)
        }
        }}/>
    
        
        {
          getValues.map( (val,idx) => <MyCard key={idx} title={data[idx].title + " " + val} marks={data[idx].mark} onChange={(e,v) => onChange(idx,v)} value={val}></MyCard>)
        }     
        {
          getAll && getAll.map( (v,idx) => <p key={idx}>{v.join(",")}</p>)
        }  
     
        </Card>
       
        </Box> 
    
    </div>
  );
}

export default App;
