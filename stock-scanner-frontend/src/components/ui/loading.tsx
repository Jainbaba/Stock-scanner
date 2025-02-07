import { CircularProgress, Box } from '@mui/material';

export function Loading() {
  return (
    <Box 
      display="flex" 
      alignItems="center" 
      justifyContent="center" 
      minHeight="100vh"
    >
      <CircularProgress />
    </Box>
  );
}
