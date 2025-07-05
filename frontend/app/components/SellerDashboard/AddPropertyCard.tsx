'use client';

import { useState } from 'react';
import { useSession } from 'next-auth/react';
import ImageUpload from './UploadImage';

const AddPropertyCard = ({ onClose }: { onClose: () => void }) => {
  const { data: session } = useSession();

  const [mainCategory, setMainCategory] = useState('property');
  const [propertyType, setPropertyType] = useState('');
  const [dealType, setDealType] = useState('');
  const [form, setForm] = useState<any>({});
  const [images, setImages] = useState<string[]>([]);

  const isResidential = mainCategory === 'property' && propertyType === 'residential';
  const isCommercial = mainCategory === 'property' && propertyType === 'commercial';
  const isAgricultural = mainCategory === 'agriculture';
  const isRent = dealType === 'rent';
  const isSell = dealType === 'sell';
  const isLease = dealType === 'lease';

  const handleChange = (field: string, value: any) => {
    setForm((prev: any) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    console.log("handle submit triggered")

    if (isAgricultural && dealType === 'rent') {
      alert('❌ Agricultural rent is not supported');
      return;
    }

    const payload: any = {
      category: isAgricultural ? 'agricultural' : propertyType,
      subcategory: dealType,
      images: images,
      title: form.title ?? '',
    };

    const detailKey =
      (isResidential && isSell && 'residential_sell') ||
      (isResidential && isRent && 'residential_rent') ||
      (isCommercial && isSell && 'commercial_sell') ||
      (isCommercial && isRent && 'commercial_rent') ||
      (isAgricultural && isLease && 'agricultural_lease') ||
      (isAgricultural && isSell && 'agricultural_sell');

    if (!detailKey) return alert('❌ Invalid form selection');

    if (form.negotiable === undefined) form.negotiable = false;
    if (form.utility_bills_included === undefined) form.utility_bills_included = false;

    const numberFields = [
      'price', 'monthly_rent', 'price_per_acre', 'rent_per_acre',
      'total_area_yards', 'area_yards', 'total_area', 'available_area',
      'advance_amount', 'lease_duration', 'bedrooms', 'bathrooms'
    ];
    for (const field of numberFields) {
      if (form[field] !== undefined && form[field] !== '') {
        form[field] = parseFloat(form[field]);
      }
    }

    const detailForm = { ...form };
    delete detailForm.title;

    payload[detailKey] = detailForm;

    // Cleanup invalid fields based on context
if (detailKey === 'residential_sell' || detailKey === 'commercial_sell' || detailKey === 'agricultural_sell' || detailKey === 'agricultural_lease') {
  delete detailForm.utility_bills_included;
}

//     const requiredRentFields = [
//   'monthly_rent', 'advance_amount', 'utility_bills_included',
//   'address', 'bedrooms', 'bathrooms'
// ];

// if(isResidential && isRent){
//   for (const field of requiredRentFields) {
//     if (!form[field] && form[field] !== false && form[field] !== 0) {
//       alert(`❌ Missing required field: ${field}`);
//       return;
//     }
//   }
// }

    try {
      console.log("FINAL PAYLOAD", JSON.stringify(payload, null, 2));
      const res = await fetch('http://localhost:8000/api/properties', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${session?.user?.accessToken}`,
        },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        alert('✅ Property added!');
        onClose();
      } else {
        console.log("PAYLOAD DETAILS",payload)
        console.log('Failed to add property:', res.status, res.statusText);
        alert('❌ Failed to add property.');
      }
    } catch (err) {
      console.error('Error:', err);
      alert('⚠️ Error occurred.');
    }
  };

  return (
    <div className="p-4 h-[90vh] flex flex-col overflow-hidden">
      <h2 className="text-xl font-semibold mb-4">Add New Listing</h2>

      {/* Scrollable form area */}
      <form onSubmit={handleSubmit} className="space-y-4 overflow-y-auto flex-1 pr-2">
        {/* Select category/type/deal */}
        <div className="flex gap-4">
          <select value={mainCategory} onChange={(e) => {
            setMainCategory(e.target.value);
            setPropertyType('');
            setDealType('');
            setForm({});
          }} className="border px-3 py-2 rounded">
            <option value="property">Property</option>
            <option value="agriculture">Agricultural Land</option>
          </select>

          {mainCategory === 'property' && (
            <select value={propertyType} onChange={(e) => {
              setPropertyType(e.target.value);
              setDealType('');
              setForm({});
            }} className="border px-3 py-2 rounded">
              <option value="">Select Type</option>
              <option value="residential">Residential</option>
              <option value="commercial">Commercial</option>
            </select>
          )}

          <select value={dealType} onChange={(e) => {
            setDealType(e.target.value);
            setForm({});
          }} className="border px-3 py-2 rounded">
            <option value="">Select Deal</option>
            {isAgricultural && <option value="lease">Muqada (Lease)</option>}
            {!isAgricultural && <option value="rent">Rent</option>}
            <option value="sell">Sell</option>
          </select>
        </div>

        {/* Title */}
        <input placeholder="Title" value={form.title ?? ''} onChange={(e) => handleChange('title', e.target.value)} required className="w-full border px-3 py-2 rounded" />

        {/* Price/Rent/Negotiable */}
        {(isRent || isSell || isLease) && (
          <div className="flex gap-4">
            <input
              placeholder={isLease ? 'Rent per Acre' : isRent ? 'Monthly Rent' : 'Price'}
              type="number"
              value={
                isLease ? form.rent_per_acre ?? '' :
                isRent ? form.monthly_rent ?? '' :
                isAgricultural ? form.price_per_acre ?? '' : form.price ?? ''
              }
              onChange={(e) => handleChange(
                isLease ? 'rent_per_acre' :
                isRent ? 'monthly_rent' :
                isAgricultural ? 'price_per_acre' : 'price',
                e.target.value
              )}
              required
              className="w-full border px-3 py-2 rounded"
            />
            <select value={form.negotiable ? 'yes' : 'no'} onChange={(e) => handleChange('negotiable', e.target.value === 'yes')} className="border px-3 py-2 rounded">
              <option value="no">Fixed</option>
              <option value="yes">Negotiable</option>
            </select>
          </div>
        )}

        {/* Rent-specific */}
        {isResidential || isCommercial && isRent && (
          <>
            <input placeholder="Advance Amount" type="number" value={form.advance_amount ?? ''} onChange={(e) => handleChange('advance_amount', e.target.value)} className="w-full border px-3 py-2 rounded" />
            <select value={form.utility_bills_included ? 'yes' : 'no'} onChange={(e) => handleChange('utility_bills_included', e.target.value === 'yes')} className="border px-3 py-2 rounded">
              <option value="yes">Utility Bills Included</option>
              <option value="no">Utility Bills Excluded</option>
            </select>
          </>
        )}

        {/* Lease-specific */}
        {isLease && (
          <input placeholder="Lease Duration (years)" type="number" value={form.lease_duration ?? ''} onChange={(e) => handleChange('lease_duration', e.target.value)} className="w-full border px-3 py-2 rounded" />
        )}

        {/* Address */}
        <input placeholder="Address" value={form.address ?? ''} onChange={(e) => handleChange('address', e.target.value)} className="w-full border px-3 py-2 rounded" required />

        {/* Residential Fields */}
        {isResidential && (
          <>
            <input placeholder="Bedrooms" type="number" value={form.bedrooms ?? ''} onChange={(e) => handleChange('bedrooms', e.target.value)} className="w-full border px-3 py-2 rounded" />
            <input placeholder="Bathrooms" type="number" value={form.bathrooms ?? ''} onChange={(e) => handleChange('bathrooms', e.target.value)} className="w-full border px-3 py-2 rounded" />
            <input placeholder="Floor Number" value={form.floor_number ?? ''} onChange={(e) => handleChange('floor_number', e.target.value)} className="w-full border px-3 py-2 rounded" />
            <input placeholder="Total Area (yards)" type="number" value={form.total_area_yards ?? ''} onChange={(e) => handleChange('total_area_yards', e.target.value)} className="w-full border px-3 py-2 rounded" />
            {isSell && (<><select value={form.documents ?? ''} onChange={(e) => handleChange('documents', e.target.value)} className="w-full border px-3 py-2 rounded">
              <option value="">Select Documents</option>
              <option value="documented">Documented</option>
              <option value="kacha">Kacha</option>
            </select></>
            )}
          </>
        )}

        {/* Commercial Fields */}
        {isCommercial && (
          <>
            <input placeholder="Area (yards)" type="number" value={form.area_yards ?? ''} onChange={(e) => handleChange('area_yards', e.target.value)} className="w-full border px-3 py-2 rounded" />
            <input placeholder="Floor Number" value={form.floor_number ?? ''} onChange={(e) => handleChange('floor_number', e.target.value)} className="w-full border px-3 py-2 rounded" />
          </>
        )}

        {/* Agricultural Fields */}
        {isAgricultural && (
          <>
            <input placeholder="Total Land Area" type="number" value={form.total_area ?? ''} onChange={(e) => handleChange('total_area', e.target.value)} className="w-full border px-3 py-2 rounded" />
            <input placeholder="Available Area" type="number" value={form.available_area ?? ''} onChange={(e) => handleChange('available_area', e.target.value)} className="w-full border px-3 py-2 rounded" />
          </>
        )}

        {/* Description */}
        <textarea placeholder="Description (optional)" value={form.description ?? ''} onChange={(e) => handleChange('description', e.target.value)} className="w-full border px-3 py-2 rounded" rows={3} />

        {/* Image upload */}
        <ImageUpload
          images={images}
          onUpload={(updatedImages) => setImages(updatedImages)}
          accessToken={session?.user?.accessToken || ''}
        />

      {/* Sticky footer for buttons */}
      <div className="flex justify-end gap-2 pt-4 sticky bottom-0 bg-white border-t mt-2">
        <button type="button" onClick={onClose} className="px-4 py-2 border rounded">Cancel</button>
        <button type="submit" className="px-4 py-1 bg-blue-600 text-white hover:cursor-pointer rounded">Add Property</button>
      </div>
      </form>
    </div>
  );
};

export default AddPropertyCard;
