import React from 'react';
import { Toast, ToastBody, ToastHeader } from 'reactstrap';

export default function Logout() {
    localStorage.clear();

    return (
        <div className="p-3 bg-primary my-2 rounded">
        <Toast>
          <ToastHeader>
            Logout
          </ToastHeader>
          <ToastBody>
            Thank you!
          </ToastBody>
        </Toast>
      </div>
    )
}

