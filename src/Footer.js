import React from 'react';
import { ScaleAppFooter } from '@telekom/scale-components-react';

function Footer(Contactname) {
    
    return (
        <div>
            <ScaleAppFooter id="Footer-React" claim-lang="en" variant="standard" footerNavigation={
                [
                    { name: "Contact", id: "Contact", href: "#contact" },
                    { name: "Terms and conditions", id: "Terms and conditions", href: "#terms-and-conditions"},
                    { name: "Legal notice", id: "Legal notice", href: "#legal-notice" },
                    {
                        name: "Data privacy",
                        id: "Data privacy",
                        href: "#data-privacy",
                        icon: "alert-imprint-dataprivacy",
                    }
                ]
            }>
            </ScaleAppFooter>
        </div> 
  );

}

export default Footer;