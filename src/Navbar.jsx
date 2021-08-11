import React from 'react';
import { ScaleAppShell } from '@telekom/scale-components-react';
import { Link } from 'react-router-dom';

function NavBar(props) {
    
    return (
        <div>
            <ScaleAppShell 
                claim-Lang="en" 
                logo-title="OpenTelekomCloud" 
                logoHref="/"
                addonNavigation={
                    [
                        {
                            "name": "Register", "href": "/"
                        },
                        {
                            "name": "Login", "href": "/login"
                        },
                        {
                            "name": "Contact", "href": "/contact"
                        },
                        {
                            "name":"Open Telekom Cloud", "href": "https://open-telekom-cloud.com/de"
                        }
                    ]
                }
            
            ></ScaleAppShell>
        </div> 
  );

}

export default NavBar;