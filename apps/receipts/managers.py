from django.db import models
from django.contrib.admin.utils import flatten


class StoreManager(models.Manager):
    def bulk_upsert(self, stores):
        """
        Bulk upsert product categories
        """
        values = ','.join(['(%s, %s, %s, %s, %s, %s, %s, %s, %s)']*len(stores))
        db_name = self.model.objects.model._meta.db_table
        params = flatten([[s.name, s.address, s.external_id,
                           s.reg_number, s.zipcode, s.country,
                           s.city, s.phone, s.merchant.pk]
                           for s in stores])
        query = """
            INSERT INTO {0} (name, address, external_id, reg_number,
                             zipcode, country, city, phone, merchant_id)
            VALUES {1}
            ON CONFLICT (name, address)
            DO
            UPDATE SET name = EXCLUDED.name RETURNING id, name, address;
        """.format(db_name, values)
        return self.model.objects.raw(query, params)


class ProductManager(models.Manager):
    def bulk_upsert(self, products):
        """
        Bulk upsert products
        """
        values = ','.join(['(%s, %s, %s)']*len(products))
        params = flatten([[p.category.pk, p.name, p.number] for p in products])
        db_name = self.model.objects.model._meta.db_table
        query = """
            INSERT INTO {0} (category_id, name, number)
            VALUES {1}
            ON CONFLICT (name)
            DO
            UPDATE SET name = EXCLUDED.name RETURNING id, name, category_id;
        """.format(db_name, values)
        return self.model.objects.raw(query, params)


class ProductCategoryManager(models.Manager):
    def bulk_upsert(self, categories):
        """
        Bulk upsert product categories
        """
        values = ','.join(['(%s)']*len(categories))
        db_name = self.model.objects.model._meta.db_table
        query = """
            INSERT INTO {0} (name)
            VALUES {1}
            ON CONFLICT (name)
            DO
            UPDATE SET name = EXCLUDED.name RETURNING id, name;
        """.format(db_name, values)
        return self.model.objects.raw(query, [c.name for c in categories])


class ArticleManager(models.Manager):

    def bulk_upsert(self, aricles):
        """
        Bulk upsert products
        """
        values = ','.join(['(%s, %s, %s)']*len(aricles))
        params = flatten([[a.product.pk, a.name, a.gtin] for a in aricles])
        db_name = self.model.objects.model._meta.db_table
        query = """
            INSERT INTO {0} (product_id, name, gtin)
            VALUES {1}
            ON CONFLICT (gtin)
            DO
            UPDATE SET name = EXCLUDED.name RETURNING id, name, product_id, gtin;
        """.format(db_name, values)
        return self.model.objects.raw(query, params)
