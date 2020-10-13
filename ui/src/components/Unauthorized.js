import React from 'react'
import { Toast, ToastBody, ToastHeader } from 'reactstrap';

export default function Unauthorized() {
    return (
        <div className="p-3 bg-danger my-2 rounded">
            <Toast>
            <ToastHeader>
                401 - UNAUTHORIZED
            </ToastHeader>
            <ToastBody>
                Login first!
            </ToastBody>
            </Toast>
        </div>

    )
}