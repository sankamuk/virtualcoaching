import React from 'react'
import { Button } from 'reactstrap'

export default function Footer() {
    return (
        <footer class="page-footer font-small unique-color-dark pt-4">
        <div class="container">
            <ul class="list-unstyled list-inline text-center py-2">
            <li class="list-inline-item">
                <h5 class="mb-1">Query</h5>
            </li>
            <li class="list-inline-item">
                <Button href="/query" color="primary">Report Here</Button>
            </li>
            </ul>
        </div>
        <div class="footer-copyright text-center py-3">© 2020 Copyright:
            <a href="https://ExamNow.com/"> ExamNow.com</a>
        </div>
        </footer>
    )
}
