import React from 'react';
import { Toast, ToastBody, ToastHeader } from 'reactstrap';

export default function InternalError() {
    localStorage.clear();

    return (
        <div className="p-3 bg-primary my-2 rounded">
        <Toast>
          <ToastHeader>
            500 - Internal Server Error
          </ToastHeader>
          <ToastBody>
            Backend Issue! 
            Try again or contact support.
          </ToastBody>
        </Toast>
      </div>
    )
}