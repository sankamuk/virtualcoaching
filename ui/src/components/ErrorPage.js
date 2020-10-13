import React from 'react';
import { Toast, ToastBody, ToastHeader } from 'reactstrap';

export default function ErrorPage() {
    localStorage.clear();

    return (
        <div className="p-3 bg-primary my-2 rounded">
        <Toast>
          <ToastHeader>
            404 - Error
          </ToastHeader>
          <ToastBody>
            No such Page!
          </ToastBody>
        </Toast>
      </div>
    )
}