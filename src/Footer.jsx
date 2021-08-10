import React from 'react';
import { ScaleAppFooter } from '@telekom/scale-components-react';

function Footer() {
    
    return (
        <div>
            <ScaleAppFooter id="Footer-React" claim-lang="en" variant="standard" footerNavigation={
                [
                    { name: "Contact", id: "Contact", href: "https://open-telekom-cloud.com/en/contact" },
                    { name: "Terms and conditions", id: "Terms and conditions", href: "https://open-telekom-cloud.com/en/data-protection"},
                    { name: "Legal notice", id: "Legal notice", href: "https://open-telekom-cloud.com/en/disclaimer-of-liability" },
                    {
                        name: "Data privacy",
                        id: "Data privacy",
                        href: "https://open-telekom-cloud.com/en/data-protection",
                        icon: "alert-imprint-dataprivacy",
                    }
                ]
            }>
            </ScaleAppFooter>
        </div> 
  );

}

export default Footer;