import React from 'react';
import { ScaleAppShell } from '@telekom/scale-components-react';

function NavBar() {
    
    return (
        <div>
            <ScaleAppShell 
                claim-Lang="en" 
                logo-title="OpenTelekomCloud" 
                logoHref="/"
                addonNavigation={
                    [
                        {
                            "name": "Contact", "href": "#contact"
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