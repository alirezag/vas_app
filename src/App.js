
import './App.css';
import MyCard from './MyCard';
import {Card, Box, Button, CardHeader, CardMedia} from '@mui/material'
import {useEffect, useState} from "react";
function App() {

  const [data, setData]= useState([ 
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
    const onChange= (idx,v) => { 
      const vs = [...getValues];
      vs[idx]=v
      setValues(vs)
    }

  useEffect(() => { 
    setData( d => [...d])
    console.log("hie")
  },[getAll])



  return (
    <div className="App">
      <header className="App-header">
        VAS
        </header>
       <Box display="flex" justifyContent="center">
       <Card >
       <CardHeader
        action={
        <Button  onClick={ (ev) => { 
          
          if (getAll) {
            setAll([...getAll, getValues]);
          } else { 
            setAll([getValues]);
          }

          fetch('http://localhost:9000', {
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
         
           
         
        }}>Save & Next</Button>}/>
        
        <CardMedia 
        component="audio"
        src="sounds/audio_sample.mp3"
        controls
        />
    
        
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
