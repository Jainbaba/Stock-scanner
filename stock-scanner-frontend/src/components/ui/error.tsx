import { Alert } from '@mui/material';

export function ErrorMessage({ message }: { message: string }) {
  return (
    <Alert severity="error" sx={{ mt: 2, mb: 2 }}>
      {message}
    </Alert>
  );
}
