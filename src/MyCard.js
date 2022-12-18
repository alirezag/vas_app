import React from 'react';
import { CardContent, Card, Slider } from '@mui/material';




export default function MyCard({title,marks,onChange,value}) {
  

  return (

      <Card sx={{width:300,m:"5px", pr:"100px", pl:"100px"}}  >
    
        <CardContent >
            {title}
            <Slider
                value={value}
                marks={marks}
                min={0}
                max={100}
                onChange={onChange}
            />
        </CardContent>

    </Card> 
     

  );
}
